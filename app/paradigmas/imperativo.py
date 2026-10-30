"""Paradigma imperativo: secuencia explícita del flujo de un pedido.

El endpoint de creación de pedidos sigue este orden: validar, crear cabecera,
guardar detalles, calcular factura, confirmar la transacción.
"""

def pasos_creacion_pedido() -> list[str]:
    pasos = []
    pasos.append("validar datos de entrada")
    pasos.append("validar productos y existencias")
    pasos.append("crear pedido")
    pasos.append("guardar detalles")
    pasos.append("calcular y guardar factura")
    pasos.append("confirmar transacción")
    return pasos
