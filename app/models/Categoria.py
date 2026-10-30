from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Categoria(Base):
    __tablename__ = "categoria"
    idCategoria: Mapped[int] = mapped_column("idcategoria", primary_key=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(225))
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    productos = relationship("Producto", back_populates="categoria")
