from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.Inventario import Inventario
from app.models.Ingrediente import Ingrediente

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.get("/")
def listar_inventario(db: Session = Depends(get_db)):
    filas = db.query(Inventario).options(joinedload(Inventario.ingrediente)).order_by(Inventario.idInventario).all()
    return [{
        "idInventario": fila.idInventario,
        "Ingrediente_idIngrediente": fila.Ingrediente_idIngrediente,
        "ingrediente": {
            "idIngrediente": fila.ingrediente.idIngrediente,
            "nombre": fila.ingrediente.nombre,
            "unidad_medida": fila.ingrediente.unidad_medida,
            "estado": fila.ingrediente.estado,
        } if fila.ingrediente else None,
        "cantidad_actual": fila.cantidad_actual,
        "cantidad_minima": fila.cantidad_minima,
        "ultima_actualizacion": fila.ultima_actualizacion,
        "stock_bajo": fila.cantidad_actual <= fila.cantidad_minima,
    } for fila in filas]

@router.patch("/{inventario_id}")
def actualizar_stock(
    inventario_id: int,
    cantidad_actual: Decimal = Body(embed=True, gt=0),
    db: Session = Depends(get_db),
):
    fila = db.get(Inventario, inventario_id)
    if not fila:
        raise HTTPException(status_code=404, detail="Registro de inventario no encontrado.")
    fila.cantidad_actual = cantidad_actual
    fila.ultima_actualizacion = datetime.now(timezone.utc).replace(tzinfo=None)
    try:
        db.commit()
        db.refresh(fila)
        return {
            "idInventario": fila.idInventario,
            "Ingrediente_idIngrediente": fila.Ingrediente_idIngrediente,
            "cantidad_actual": fila.cantidad_actual,
            "cantidad_minima": fila.cantidad_minima,
            "ultima_actualizacion": fila.ultima_actualizacion,
            "stock_bajo": fila.cantidad_actual <= fila.cantidad_minima,
        }
    except Exception:
        db.rollback()
        raise
