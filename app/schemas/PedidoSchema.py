from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, model_validator

class DetallePedidoCreate(BaseModel):
    Producto_idProducto: int = Field(gt=0)
    cantidad: int = Field(gt=0, le=1000)

class PedidoCreate(BaseModel):
    Cliente_idCliente: int | None = Field(default=None, gt=0)
    Mesa_idMesa: int | None = Field(default=None, gt=0)
    MetodoPago_idMetodoPago: int | None = Field(default=None, gt=0)
    Empleado_idEmpleado: int | None = Field(default=None, gt=0)
    descuento: Decimal = Field(default=Decimal("0"), ge=0, max_digits=10, decimal_places=2)
    detalles: list[DetallePedidoCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def productos_sin_duplicados(self):
        ids = [d.Producto_idProducto for d in self.detalles]
        if len(ids) != len(set(ids)):
            raise ValueError("No repitas productos en los detalles del pedido; suma sus cantidades.")
        return self

class EstadoPedidoUpdate(BaseModel):
    estado: str = Field(min_length=1, max_length=1)
