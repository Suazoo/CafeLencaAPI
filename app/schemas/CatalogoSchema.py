from pydantic import BaseModel, ConfigDict, Field

class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=45)
    descripcion: str | None = Field(default=None, max_length=225)
    estado: str = Field(default="1", min_length=1, max_length=1)

class CategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idCategoria: int
    nombre: str
    descripcion: str | None = None
    estado: str

class MesaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idMesa: int
    numero: int
    capacidad: int
    estado: str

class MetodoPagoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idMetodoPago: int
    nombre: str
    estado: str
