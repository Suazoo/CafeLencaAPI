"""Paradigma lógico: reglas expresadas como condiciones verificables.

Las reglas ejecutables viven en app.motor_logico.reglas y se usan al crear
pedidos.
"""
from app.motor_logico.reglas import producto_activo, cantidad_valida

def puede_venderse(producto, cantidad: int) -> bool:
    return inferir_venta(hechos_producto(producto, cantidad))["puede_venderse"]


def hechos_producto(producto, cantidad: int) -> dict[str, bool]:
    """Construye los hechos que serán evaluados por las reglas de venta."""
    return {
        "producto_activo": producto_activo(producto),
        "cantidad_valida": cantidad_valida(cantidad),
    }


def inferir_venta(hechos: dict[str, bool]) -> dict[str, bool | str]:
    """Aplica reglas a hechos y devuelve la conclusión y su explicación."""
    puede_venderse = (
        hechos.get("producto_activo", False)
        and hechos.get("cantidad_valida", False)
    )
    return {
        **hechos,
        "puede_venderse": puede_venderse,
        "motivo": (
            "El producto cumple las reglas de venta."
            if puede_venderse
            else "El producto no cumple las reglas de venta."
        ),
    }

def reglas_disponibilidad() -> list[str]:
    return [
        "un producto se vende si su estado está activo",
        "la cantidad solicitada debe ser mayor que cero",
        "si hay receta configurada, debe existir inventario suficiente",
    ]
