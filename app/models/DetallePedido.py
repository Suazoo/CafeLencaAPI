from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class DetallePedido(Base):
    __tablename__ = "detallepedido"
    Producto_idProducto: Mapped[int] = mapped_column(
        "producto_idproducto", ForeignKey("producto.idproducto", ondelete="CASCADE"), primary_key=True
    )
    Pedido_idPedido: Mapped[int] = mapped_column(
        "pedido_idpedido", ForeignKey("pedido.idpedido", ondelete="CASCADE"), primary_key=True
    )
    cantidad: Mapped[int] = mapped_column(nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    producto = relationship("Producto", back_populates="detalles_pedido")
    pedido = relationship("Pedido", back_populates="detalles")
