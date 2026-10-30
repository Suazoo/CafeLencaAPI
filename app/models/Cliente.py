from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "cliente"
    idCliente: Mapped[int] = mapped_column("idcliente", primary_key=True)
    Persona_idPersona: Mapped[int] = mapped_column(
        "persona_idpersona", ForeignKey("persona.idpersona", ondelete="CASCADE"),
        nullable=False, unique=True
    )
    persona = relationship("Persona", back_populates="cliente")
    preferencias = relationship("PreferenciaCliente", back_populates="cliente", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")
