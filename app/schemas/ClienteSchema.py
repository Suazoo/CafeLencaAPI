from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ClienteCreate(BaseModel):
    Pnombre: str = Field(min_length=1, max_length=45)
    Snombre: str | None = Field(default=None, max_length=45)
    Papellido: str = Field(min_length=1, max_length=45)
    Sapellido: str | None = Field(default=None, max_length=45)
    correo: EmailStr
    telefono: str | None = Field(default=None, max_length=45)

class ClienteUpdate(BaseModel):
    Pnombre: str | None = Field(default=None, min_length=1, max_length=45)
    Snombre: str | None = Field(default=None, max_length=45)
    Papellido: str | None = Field(default=None, min_length=1, max_length=45)
    Sapellido: str | None = Field(default=None, max_length=45)
    correo: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=45)

class PersonaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idPersona: int
    Pnombre: str
    Snombre: str | None = None
    Papellido: str
    Sapellido: str | None = None
    correo: str
    Fecha_registro: datetime

class ClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idCliente: int
    Persona_idPersona: int
    persona: PersonaResponse
