from sqlalchemy.orm import Session
from app.models.Producto import Producto
from app.models.Categoria import Categoria
from app.motor_logico.reglas import ESTADOS_ACTIVOS
from app.paradigmas.declarativo import productos_activos

class ProductoService:
    @staticmethod
    def obtener_productos(db: Session):
        return db.query(Producto).order_by(Producto.idProducto).all()

    @staticmethod
    def obtener_productos_disponibles(db: Session):
        return productos_activos(db)

    @staticmethod
    def obtener_producto(db: Session, producto_id: int):
        return db.query(Producto).filter(Producto.idProducto == producto_id).first()

    @staticmethod
    def crear_producto(db: Session, datos: dict):
        if datos.get("Categoria_idCategoria") is not None and not db.get(Categoria, datos["Categoria_idCategoria"]):
            raise ValueError("La categoría indicada no existe.")
        producto = Producto(**datos)
        db.add(producto)
        try:
            db.commit()
            db.refresh(producto)
            return producto
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def actualizar_producto(db: Session, producto_id: int, datos: dict):
        producto = ProductoService.obtener_producto(db, producto_id)
        if not producto:
            return None
        if datos.get("Categoria_idCategoria") is not None and not db.get(Categoria, datos["Categoria_idCategoria"]):
            raise ValueError("La categoría indicada no existe.")
        for key, value in datos.items():
            setattr(producto, key, value)
        try:
            db.commit()
            db.refresh(producto)
            return producto
        except Exception:
            db.rollback()
            raise
