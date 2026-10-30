"""Paradigma declarativo: el ORM describe qué datos y relaciones existen.
"""
from sqlalchemy.orm import Session
from app.models.Producto import Producto
from app.models.Categoria import Categoria

def productos_activos(db: Session):
    return db.query(Producto).filter(Producto.estado.in_(("1", "A", "a"))).order_by(Producto.nombre).all()

def categorias_activas(db: Session):
    return db.query(Categoria).filter(Categoria.estado.in_(("1", "A", "a"))).order_by(Categoria.nombre).all()
