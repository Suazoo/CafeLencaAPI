from datetime import datetime
from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Persona(Base):
    __tablename__ = "persona"
    idPersona: Mapped[int] = mapped_column("idpersona", primary_key=True)
    Pnombre: Mapped[str] = mapped_column("pnombre", String(45), nullable=False)
    Snombre: Mapped[str | None] = mapped_column("snombre", String(45))
    Papellido: Mapped[str] = mapped_column("papellido", String(45), nullable=False)
    Sapellido: Mapped[str | None] = mapped_column("sapellido", String(45))
    correo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    Fecha_registro: Mapped[datetime] = mapped_column(
        "fecha_registro", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    telefonos = relationship("Telefono", back_populates="persona", cascade="all, delete-orphan")
    cliente = relationship("Cliente", back_populates="persona", uselist=False, cascade="all, delete-orphan")
    empleado = relationship("Empleado", back_populates="persona", uselist=False, cascade="all, delete-orphan")
