from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Rol_has_Empleado(Base):
    __tablename__ = "rol_has_empleado"
    Rol_idRol: Mapped[int] = mapped_column(
        "rol_idrol", ForeignKey("rol.idrol", ondelete="CASCADE"), primary_key=True
    )
    Empleado_idEmpleado: Mapped[int] = mapped_column(
        "empleado_idempleado", ForeignKey("empleado.idempleado", ondelete="CASCADE"), primary_key=True
    )
    rol = relationship("Rol", back_populates="empleados")
    empleado = relationship("Empleado", back_populates="roles")
