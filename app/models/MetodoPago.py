from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class MetodoPago(Base):
    __tablename__ = "metodopago"
    idMetodoPago: Mapped[int] = mapped_column("idmetodopago", primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    pedidos = relationship("Pedido", back_populates="metodo_pago")
