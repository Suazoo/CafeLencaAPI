from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Ingrediente(Base):
    __tablename__ = "ingrediente"
    idIngrediente: Mapped[int] = mapped_column("idingrediente", primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String(25), nullable=False)
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    inventario = relationship("Inventario", back_populates="ingrediente", uselist=False, cascade="all, delete-orphan")
    productos = relationship("Ingrediente_has_Producto", back_populates="ingrediente", cascade="all, delete-orphan")
