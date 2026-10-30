from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Mesa(Base):
    __tablename__ = "mesa"
    idMesa: Mapped[int] = mapped_column("idmesa", primary_key=True)
    numero: Mapped[int] = mapped_column(nullable=False, unique=True)
    capacidad: Mapped[int] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    reservas = relationship("Reserva", back_populates="mesa")
    pedidos = relationship("Pedido", back_populates="mesa")
