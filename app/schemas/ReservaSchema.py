from datetime import datetime
from pydantic import BaseModel, Field

class ReservaCreate(BaseModel):
    fecha_reserva: datetime
    cantidad_persona: int = Field(gt=0, le=50)
    Cliente_idCliente: int = Field(gt=0)
    Mesa_idMesa: int | None = Field(default=None, gt=0)
    estado: str = Field(default="1", min_length=1, max_length=1)

class ReservaResponse(BaseModel):
    idReserva: int
    fecha_reserva: datetime
    cantidad_persona: int
    estado: str
    Cliente_idCliente: int | None = None
    Mesa_idMesa: int | None = None

    class Config:
        from_attributes = True
