from sqlalchemy.orm import Session

from app.models.Producto import Producto


class ProductoRepository:

    @staticmethod
    def obtener_todos(db: Session):
        return db.query(Producto).all()

    @staticmethod
    def obtener_disponibles(db: Session):
        return (
            db.query(Producto)
            .filter(Producto.estado == "A")
            .all()
        )

    @staticmethod
    def obtener_por_id(db: Session, producto_id: int):
        return (
            db.query(Producto)
            .filter(Producto.idProducto == producto_id)
            .first()
        )