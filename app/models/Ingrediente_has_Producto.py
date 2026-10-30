from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Ingrediente_has_Producto(Base):
    __tablename__ = "ingrediente_has_producto"
    Ingrediente_idIngrediente: Mapped[int] = mapped_column(
        "ingrediente_idingrediente", ForeignKey("ingrediente.idingrediente", ondelete="CASCADE"), primary_key=True
    )
    Producto_idProducto: Mapped[int] = mapped_column(
        "producto_idproducto", ForeignKey("producto.idproducto", ondelete="CASCADE"), primary_key=True
    )
    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    ingrediente = relationship("Ingrediente", back_populates="productos")
    producto = relationship("Producto", back_populates="ingredientes")
