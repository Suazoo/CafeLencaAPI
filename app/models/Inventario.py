from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Inventario(Base):
    __tablename__ = "inventario"
    idInventario: Mapped[int] = mapped_column("idinventario", primary_key=True)
    cantidad_actual: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    cantidad_minima: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    ultima_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    Ingrediente_idIngrediente: Mapped[int] = mapped_column(
        "ingrediente_idingrediente", ForeignKey("ingrediente.idingrediente", ondelete="CASCADE"),
        nullable=False, unique=True
    )
    ingrediente = relationship("Ingrediente", back_populates="inventario")
