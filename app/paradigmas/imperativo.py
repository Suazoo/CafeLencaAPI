"""Demostración académica del paradigma imperativo."""

def pasos_creacion_pedido() -> list[str]:
    pasos = []
    pasos.append("validar datos de entrada")
    pasos.append("validar productos y existencias")
    pasos.append("crear pedido")
    pasos.append("guardar detalles")
    pasos.append("calcular y guardar factura")
    pasos.append("confirmar transacción")
    return pasos


def evaluar_ventas_diarias(ventas: list[float], meta: float) -> dict[str, float | int | str]:
    """Usa variables, ciclo, condicionales y una secuencia explícita."""
    total = 0.0
    cantidad = 0
    for venta in ventas:
        if venta > 0:
            total += venta
            cantidad += 1

    promedio = total / cantidad if cantidad else 0.0
    estado = "meta alcanzada" if total >= meta else "meta pendiente"
    return {
        "total": round(total, 2),
        "cantidad": cantidad,
        "promedio": round(promedio, 2),
        "estado": estado,
    }
