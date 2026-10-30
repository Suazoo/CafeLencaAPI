from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class PreferenciaCliente(Base):
    __tablename__ = "preferenciacliente"
    idPreferencia: Mapped[int] = mapped_column("idpreferencia", primary_key=True)
    tipo_preferencia: Mapped[str] = mapped_column(String(45), nullable=False)
    valor: Mapped[str] = mapped_column(String(100), nullable=False)
    Cliente_idCliente: Mapped[int] = mapped_column(
        "cliente_idcliente", ForeignKey("cliente.idcliente", ondelete="CASCADE"), nullable=False
    )
    cliente = relationship("Cliente", back_populates="preferencias")
