"""Registro central de los modelos ORM existentes de Café Lenca."""
from app.models.Persona import Persona
from app.models.Telefono import Telefono
from app.models.Cliente import Cliente
from app.models.Empleado import Empleado
from app.models.Rol import Rol
from app.models.Rol_has_Empleado import Rol_has_Empleado
from app.models.Categoria import Categoria
from app.models.Producto import Producto
from app.models.Ingrediente import Ingrediente
from app.models.Ingrediente_has_Producto import Ingrediente_has_Producto
from app.models.Inventario import Inventario
from app.models.Mesa import Mesa
from app.models.MetodoPago import MetodoPago
from app.models.Pedido import Pedido
from app.models.DetallePedido import DetallePedido
from app.models.Reserva import Reserva
from app.models.Factura import Factura
from app.models.PreferenciaCliente import PreferenciaCliente

__all__ = [
    "Persona", "Telefono", "Cliente", "Empleado", "Rol", "Rol_has_Empleado",
    "Categoria", "Producto", "Ingrediente", "Ingrediente_has_Producto",
    "Inventario", "Mesa", "MetodoPago", "Pedido", "DetallePedido", "Reserva",
    "Factura", "PreferenciaCliente",
]
