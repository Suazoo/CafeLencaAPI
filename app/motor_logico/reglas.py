"""Motor lógico de reglas de negocio de Café Lenca."""
from decimal import Decimal
from sqlalchemy import exists, or_, select
from sqlalchemy.orm import Session
from app.models.Producto import Producto
from app.models.Ingrediente_has_Producto import Ingrediente_has_Producto
from app.models.Inventario import Inventario

ESTADOS_ACTIVOS = {"1", "A", "a", "ACTIVO", "activo"}

def producto_activo(producto: Producto) -> bool:
    return str(producto.estado).strip() in ESTADOS_ACTIVOS

def cantidad_valida(cantidad: int) -> bool:
    return isinstance(cantidad, int) and not isinstance(cantidad, bool) and cantidad > 0

def validar_producto_vendible(producto: Producto, cantidad: int) -> None:
    if not producto_activo(producto):
        raise ValueError(f"El producto '{producto.nombre}' está inactivo.")
    if not cantidad_valida(cantidad):
        raise ValueError("La cantidad debe ser un entero mayor que cero.")

def validar_y_descontar_receta(db: Session, producto_id: int, cantidad_producto: int) -> list[str]:
    """Valida y descuenta ingredientes cuando el producto tiene receta configurada.
    """
    receta = (
        db.query(Ingrediente_has_Producto)
        .filter(Ingrediente_has_Producto.Producto_idProducto == producto_id)
        .all()
    )
    alertas = []
    for componente in receta:
        inventario = (
            db.query(Inventario)
            .filter(Inventario.Ingrediente_idIngrediente == componente.Ingrediente_idIngrediente)
            .with_for_update()
            .first()
        )
        requerido = Decimal(str(componente.cantidad)) * Decimal(cantidad_producto)
        if inventario is None:
            raise ValueError(
                f"Falta configurar inventario para el ingrediente ID {componente.Ingrediente_idIngrediente}."
            )
        disponible = Decimal(str(inventario.cantidad_actual))
        if disponible < requerido:
            raise ValueError(
                f"Inventario insuficiente para el ingrediente ID {componente.Ingrediente_idIngrediente}; "
                f"se requiere {requerido} y hay {disponible}."
            )
        inventario.cantidad_actual = disponible - requerido
        if inventario.cantidad_actual <= Decimal(str(inventario.cantidad_minima)):
            alertas.append(f"Inventario bajo para ingrediente ID {componente.Ingrediente_idIngrediente}.")
    return alertas

def recomendar_productos(db: Session, limite: int = 5):
    """Devuelve productos activos que pueden prepararse con el inventario actual."""
    limite = max(1, min(int(limite), 20))
    ingredientes_sin_stock = (
        select(Ingrediente_has_Producto.Producto_idProducto)
        .outerjoin(
            Inventario,
            Inventario.Ingrediente_idIngrediente
            == Ingrediente_has_Producto.Ingrediente_idIngrediente,
        )
        .where(
            or_(
                Inventario.idInventario.is_(None),
                Inventario.cantidad_actual < Ingrediente_has_Producto.cantidad,
            )
        )
        .distinct()
        .subquery()
    )
    return (
        db.query(Producto)
        .filter(
            Producto.estado.in_(tuple(ESTADOS_ACTIVOS)),
            ~exists().where(
                Producto.idProducto == ingredientes_sin_stock.c.Producto_idProducto
            ),
        )
        .order_by(Producto.precio, Producto.nombre)
        .limit(limite)
        .all()
    )
