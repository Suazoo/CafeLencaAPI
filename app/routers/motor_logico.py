import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.motor_logico.reglas import recomendar_productos
from app.paradigmas.logico import reglas_disponibilidad

router = APIRouter(prefix="/motor-logico", tags=["Motor lógico"])

class SolicitudIA(BaseModel):
    solicitud: str = Field(min_length=3, max_length=500)
    limite: int = Field(default=5, ge=1, le=10)

@router.get("/recomendaciones")
def recomendaciones(limite: int = Query(default=5, ge=1, le=20), db: Session = Depends(get_db)):
    productos = recomendar_productos(db, limite)
    return [{
        "idProducto": p.idProducto,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio": p.precio,
        "Categoria_idCategoria": p.Categoria_idCategoria,
        "motivo": "Producto activo recomendado por disponibilidad y precio.",
    } for p in productos]

@router.get("/reglas")
def listar_reglas():
    return {"motor": "Café Lenca", "reglas": reglas_disponibilidad()}

@router.post("/ia")
def recomendacion_ia(datos: SolicitudIA, db: Session = Depends(get_db)):
    """Interpreta la solicitud usando productos previamente validados por el motor lógico."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="La integración de IA no está configurada en el servidor.")

    productos = recomendar_productos(db, 20)
    catalogo = [
        {
            "idProducto": producto.idProducto,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": float(producto.precio),
        }
        for producto in productos
    ]
    prompt = (
        "Eres un asistente de ventas para Café Lenca. Selecciona como máximo "
        f"{datos.limite} productos del catálogo que respondan a la solicitud. "
        "Solo puedes usar los idProducto incluidos. No inventes productos, precios "
        'ni ingredientes. Responde únicamente JSON válido con esta forma: '
        '{"mensaje":"respuesta breve en español","productos":[{"idProducto":1,"razon":"razón breve"}]}. '
        f"Solicitud del cliente: {datos.solicitud}\n"
        f"Catálogo validado:\n{json.dumps(catalogo, ensure_ascii=False)}"
    )
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    request = Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}",
        data=json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            respuesta = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detalle = ""
        try:
            cuerpo = json.loads(exc.read().decode("utf-8"))
            detalle = cuerpo.get("error", {}).get("message", "")
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        if exc.code in (401, 403):
            raise HTTPException(status_code=502, detail="La clave de Gemini no es válida o no tiene permisos.") from exc
        if exc.code == 429:
            raise HTTPException(status_code=503, detail="Gemini alcanzó temporalmente su límite gratuito.") from exc
        raise HTTPException(status_code=502, detail=f"Gemini no pudo procesar la solicitud{f': {detalle}' if detalle else '.'}") from exc
    except (TimeoutError, URLError) as exc:
        raise HTTPException(status_code=504, detail="Gemini no respondió a tiempo.") from exc

    try:
        texto = respuesta["candidates"][0]["content"]["parts"][0]["text"]
        resultado = json.loads(texto)
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail="Gemini devolvió una respuesta inválida.") from exc

    productos_validos = {producto["idProducto"]: producto for producto in catalogo}
    recomendaciones = []
    for sugerencia in resultado.get("productos", []):
        producto = productos_validos.get(sugerencia.get("idProducto"))
        if producto:
            recomendaciones.append({
                **producto,
                "motivo": sugerencia.get("razon", "Coincide con la solicitud del cliente."),
            })
    return {
        "mensaje": str(resultado.get("mensaje", "Estas opciones pueden interesarle al cliente.")),
        "productos": recomendaciones[:datos.limite],
        "motor_principal": True,
        "ia": modelo,
    }
