from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Empleado(Base):
    __tablename__ = "empleado"
    idEmpleado: Mapped[int] = mapped_column("idempleado", primary_key=True)
    Persona_idPersona: Mapped[int] = mapped_column(
        "persona_idpersona", ForeignKey("persona.idpersona", ondelete="CASCADE"),
        nullable=False, unique=True
    )
    persona = relationship("Persona", back_populates="empleado")
    roles = relationship("Rol_has_Empleado", back_populates="empleado", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="empleado")
