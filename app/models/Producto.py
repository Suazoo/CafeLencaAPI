from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Producto(Base):
    __tablename__ = "producto"
    idProducto: Mapped[int] = mapped_column("idproducto", primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(225))
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    Categoria_idCategoria: Mapped[int | None] = mapped_column(
        "categoria_idcategoria", ForeignKey("categoria.idcategoria", ondelete="SET NULL"), nullable=True
    )
    categoria = relationship("Categoria", back_populates="productos")
    detalles_pedido = relationship("DetallePedido", back_populates="producto")
    ingredientes = relationship("Ingrediente_has_Producto", back_populates="producto", cascade="all, delete-orphan")
