from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=45)
    descripcion: str | None = Field(default=None, max_length=225)
    precio: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    estado: str = Field(default="1", min_length=1, max_length=1)
    Categoria_idCategoria: int | None = None

class ProductoUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=45)
    descripcion: str | None = Field(default=None, max_length=225)
    precio: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    estado: str | None = Field(default=None, min_length=1, max_length=1)
    Categoria_idCategoria: int | None = None

class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    idProducto: int
    nombre: str
    descripcion: str | None = None
    precio: Decimal
    estado: str
    Categoria_idCategoria: int | None = None
