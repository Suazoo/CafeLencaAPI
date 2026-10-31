"""Paradigma funcional: funciones puras usadas por el caso de uso de pedidos."""
from collections.abc import Iterable
from decimal import Decimal, ROUND_HALF_UP
from functools import reduce

CENTAVO = Decimal("0.01")

def dinero(valor: Decimal | int | float | str) -> Decimal:
    return Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_UP)

def calcular_totales(subtotal: Decimal, descuento: Decimal, tasa_impuesto: Decimal) -> dict[str, Decimal]:
    """Calcula importes sin modificar estado externo (función pura)."""
    subtotal = dinero(subtotal)
    descuento = dinero(descuento)
    tasa_impuesto = Decimal(str(tasa_impuesto))
    base_imponible = dinero(subtotal - descuento)
    impuesto = dinero(base_imponible * tasa_impuesto)
    return {
        "subtotal": subtotal,
        "descuento": descuento,
        "impuesto": impuesto,
        "total": dinero(base_imponible + impuesto),
    }

def normalizar_texto(texto: str | None) -> str:
    return " ".join((texto or "").strip().split())


def importes_detalles(detalles: Iterable[dict]) -> list[Decimal]:
    """Calcula importes sin modificar la colección original."""
    return list(map(
        lambda detalle: dinero(
            detalle["precio_unitario"] * detalle["cantidad"]
        ),
        detalles,
    ))


def productos_activos(productos: Iterable) -> list:
    """Filtra productos activos sin modificar la colección original."""
    return list(filter(
        lambda producto: str(producto.estado).strip().upper() in {"1", "A", "ACTIVO"},
        productos,
    ))


def total_importes(importes: Iterable[Decimal]) -> Decimal:
    """Suma importes con reduce y devuelve un valor monetario normalizado."""
    return dinero(reduce(
        lambda acumulado, importe: acumulado + importe,
        importes,
        Decimal("0.00"),
    ))


def sumar_hasta(numero: int) -> int:
    """Ejemplo de recursividad para sumar del uno hasta ``numero``."""
    if numero <= 0:
        return 0
    return numero + sumar_hasta(numero - 1)
