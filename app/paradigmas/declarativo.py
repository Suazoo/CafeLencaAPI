"""Demostración académica de consultas declarativas con SQLAlchemy."""

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.DetallePedido import DetallePedido
from app.models.Producto import Producto
from app.models.Categoria import Categoria

def productos_activos(db: Session):
    return db.query(Producto).filter(Producto.estado.in_(("1", "A", "a"))).order_by(Producto.nombre).all()

def categorias_activas(db: Session):
    return db.query(Categoria).filter(Categoria.estado.in_(("1", "A", "a"))).order_by(Categoria.nombre).all()


def ventas_por_producto(db: Session):
    """Describe qué agrupación y ordenamiento se necesitan, sin bucles manuales."""
    return (
        db.query(
            Producto.idProducto,
            Producto.nombre,
            func.sum(DetallePedido.cantidad).label("unidades"),
        )
        .join(DetallePedido, DetallePedido.Producto_idProducto == Producto.idProducto)
        .group_by(Producto.idProducto, Producto.nombre)
        .order_by(func.sum(DetallePedido.cantidad).desc(), Producto.nombre)
        .all()
    )
