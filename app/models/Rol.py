from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Rol(Base):
    __tablename__ = "rol"
    idRol: Mapped[int] = mapped_column("idrol", primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    empleados = relationship("Rol_has_Empleado", back_populates="rol", cascade="all, delete-orphan")
