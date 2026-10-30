import json
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.motor_logico.reglas import recomendar_productos
from app.paradigmas.logico import reglas_disponibilidad
from app.services.ia_service import consultar_gemini

router = APIRouter(prefix="/motor-logico", tags=["Motor lógico"])

class SolicitudIA(BaseModel):
    solicitud: str = Field(min_length=3, max_length=500)
    limite: int = Field(default=5, ge=1, le=10)

class DatosIA(BaseModel):
    datos: dict

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
    resultado = consultar_gemini(prompt)

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
        "ia": "gemini",
    }

@router.post("/ia/pedido")
def asistente_pedido(datos: SolicitudIA, db: Session = Depends(get_db)):
    productos = recomendar_productos(db, 20)
    catalogo = [{"idProducto": p.idProducto, "nombre": p.nombre, "precio": float(p.precio), "descripcion": p.descripcion} for p in productos]
    resultado = consultar_gemini(
        "Eres asistente de pedidos de Café Lenca. Convierte la solicitud en una propuesta usando "
        "solo el catálogo. Devuelve JSON con mensaje y productos, donde cada producto contiene "
        "idProducto, cantidad y razon. No inventes productos ni precios. "
        f"Solicitud: {datos.solicitud}\nCatálogo: {json.dumps(catalogo, ensure_ascii=False)}"
    )
    validos = {p["idProducto"]: p for p in catalogo}
    lineas = []
    for item in resultado.get("productos", []):
        producto = validos.get(item.get("idProducto"))
        if producto and isinstance(item.get("cantidad"), int) and item["cantidad"] > 0:
            lineas.append({**producto, "cantidad": item["cantidad"], "motivo": item.get("razon", "Coincide con la solicitud.")})
    return {"mensaje": resultado.get("mensaje", "Propuesta lista."), "productos": lineas[:datos.limite], "motor_principal": True}

@router.post("/ia/resumen-ventas")
def resumen_ventas_ia(datos: DatosIA):
    resultado = consultar_gemini(
        "Eres analista de ventas de Café Lenca. Resume estos datos en español claro. "
        'Devuelve JSON con resumen, puntos_clave y recomendacion. No inventes cifras.\n'
        f"Datos: {json.dumps(datos.datos, ensure_ascii=False)}"
    )
    return resultado

@router.post("/ia/alertas-inventario")
def alertas_inventario_ia(datos: DatosIA):
    resultado = consultar_gemini(
        "Eres encargado de inventario de Café Lenca. Prioriza las alertas recibidas. "
        'Devuelve JSON con resumen y alertas, cada una con ingrediente, prioridad y accion. '
        "No inventes cantidades.\n"
        f"Inventario: {json.dumps(datos.datos, ensure_ascii=False)}"
    )
    return resultado
