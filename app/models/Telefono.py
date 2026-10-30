from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Telefono(Base):
    __tablename__ = "telefono"
    idTelefono: Mapped[int] = mapped_column("idtelefono", primary_key=True)
    numero: Mapped[str] = mapped_column(String(45), nullable=False)
    Persona_idPersona: Mapped[int] = mapped_column(
        "persona_idpersona", ForeignKey("persona.idpersona", ondelete="CASCADE"), nullable=False
    )
    persona = relationship("Persona", back_populates="telefonos")
