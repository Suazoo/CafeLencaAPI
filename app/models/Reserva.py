from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Reserva(Base):
    __tablename__ = "reserva"
    idReserva: Mapped[int] = mapped_column("idreserva", primary_key=True)
    fecha_reserva: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cantidad_persona: Mapped[int] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    Cliente_idCliente: Mapped[int | None] = mapped_column(
        "cliente_idcliente", ForeignKey("cliente.idcliente", ondelete="CASCADE"), nullable=True
    )
    Mesa_idMesa: Mapped[int | None] = mapped_column(
        "mesa_idmesa", ForeignKey("mesa.idmesa", ondelete="SET NULL"), nullable=True
    )
    cliente = relationship("Cliente", back_populates="reservas")
    mesa = relationship("Mesa", back_populates="reservas")
