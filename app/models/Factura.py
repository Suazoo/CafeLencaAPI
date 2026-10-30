from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Factura(Base):
    __tablename__ = "factura"
    idFactura: Mapped[int] = mapped_column("idfactura", primary_key=True)
    numero_factura: Mapped[str] = mapped_column(String(45), nullable=False, unique=True)
    fecha_emision: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descuento: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default=text("0"))
    impuesto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    Pedido_idPedido: Mapped[int] = mapped_column(
        "pedido_idpedido", ForeignKey("pedido.idpedido", ondelete="CASCADE"), nullable=False, unique=True
    )
    pedido = relationship("Pedido", back_populates="factura")
