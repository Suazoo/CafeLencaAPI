from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.Cliente import Cliente
from app.models.Producto import Producto
from app.models.Pedido import Pedido
from app.models.Reserva import Reserva
from app.models.Factura import Factura
from app.motor_logico.reglas import ESTADOS_ACTIVOS

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/resumen")
def resumen(db: Session = Depends(get_db)):
    return {
        "clientes": db.query(func.count(Cliente.idCliente)).scalar() or 0,
        "productos": db.query(func.count(Producto.idProducto)).filter(Producto.estado.in_(tuple(ESTADOS_ACTIVOS))).scalar() or 0,
        "pedidos": db.query(func.count(Pedido.idPedido)).scalar() or 0,
        "reservas": db.query(func.count(Reserva.idReserva)).scalar() or 0,
        "facturacion_total": float(db.query(func.coalesce(func.sum(Factura.total), 0)).scalar() or 0),
    }
