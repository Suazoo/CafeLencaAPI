from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.motor_logico.reglas import recomendar_productos
from app.paradigmas.logico import reglas_disponibilidad

router = APIRouter(prefix="/motor-logico", tags=["Motor lógico"])

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
