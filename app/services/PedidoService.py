"""Casos de uso de pedidos y facturación."""
import json
import os
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session, joinedload
from app.models.Pedido import Pedido
from app.models.DetallePedido import DetallePedido
from app.paradigmas.funcional import dinero

class PedidoService:
    @staticmethod
    def _query(db: Session):
        return db.query(Pedido).options(
            joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
            joinedload(Pedido.factura),
        )

    @staticmethod
    def obtener_todos(db: Session):
        return PedidoService._query(db).order_by(Pedido.idPedido.desc()).all()

    @staticmethod
    def obtener_por_id(db: Session, pedido_id: int):
        return PedidoService._query(db).filter(Pedido.idPedido == pedido_id).first()

    @staticmethod
    def crear(db: Session, datos: dict):
        try:
            tasa = float(os.getenv("TAX_RATE", "0.15"))
        except ValueError as exc:
            raise ValueError("TAX_RATE debe ser un número entre 0 y 1.") from exc
        if not 0 <= tasa <= 1:
            raise ValueError("TAX_RATE debe estar entre 0 y 1.")

        payload = {
            "cliente_id": datos.get("Cliente_idCliente"),
            "mesa_id": datos.get("Mesa_idMesa"),
            "metodo_pago_id": datos.get("MetodoPago_idMetodoPago"),
            "empleado_id": datos.get("Empleado_idEmpleado"),
            "descuento": str(datos.get("descuento", 0)),
            "tasa_impuesto": tasa,
            "detalles": [
                {
                    "producto_id": detalle["Producto_idProducto"],
                    "cantidad": detalle["cantidad"],
                }
                for detalle in datos["detalles"]
            ],
        }
        try:
            resultado = db.execute(
                text("SELECT public.registrar_pedido(CAST(:payload AS jsonb))"),
                {"payload": json.dumps(payload)},
            )
            datos_rpc = resultado.scalar_one()
            db.commit()
            pedido = PedidoService.obtener_por_id(db, datos_rpc["pedido_id"])
            if pedido is None:
                raise RuntimeError("La función de pedidos no devolvió el pedido creado.")
            return {
                "pedido": pedido,
                "alertas_inventario": datos_rpc.get("alertas_inventario", []),
            }
        except DBAPIError as exc:
            db.rollback()
            diagnostico = getattr(exc.orig, "diag", None)
            if getattr(diagnostico, "sqlstate", None) == "P0001":
                raise ValueError(
                    getattr(diagnostico, "message_primary", "No se pudo validar el pedido.")
                ) from exc
            raise

    @staticmethod
    def actualizar_estado(db: Session, pedido_id: int, estado: str):
        pedido = db.get(Pedido, pedido_id)
        if not pedido:
            return None
        pedido.estado = estado
        try:
            db.commit()
            return PedidoService.obtener_por_id(db, pedido_id)
        except Exception:
            db.rollback()
            raise

def pedido_a_dict(pedido: Pedido) -> dict:
    factura = pedido.factura
    return {
        "idPedido": pedido.idPedido,
        "fecha_pedido": pedido.fecha_pedido,
        "estado": pedido.estado,
        "Cliente_idCliente": pedido.Cliente_idCliente,
        "Mesa_idMesa": pedido.Mesa_idMesa,
        "MetodoPago_idMetodoPago": pedido.MetodoPago_idMetodoPago,
        "Empleado_idEmpleado": pedido.Empleado_idEmpleado,
        "detalles": [
            {
                "Producto_idProducto": d.Producto_idProducto,
                "nombre_producto": d.producto.nombre if d.producto else None,
                "cantidad": d.cantidad,
                "precio_unitario": d.precio_unitario,
                "importe": dinero(d.precio_unitario * d.cantidad),
            }
            for d in pedido.detalles
        ],
        "factura": None if factura is None else {
            "idFactura": factura.idFactura,
            "numero_factura": factura.numero_factura,
            "fecha_emision": factura.fecha_emision,
            "subtotal": factura.subtotal,
            "descuento": factura.descuento,
            "impuesto": factura.impuesto,
            "total": factura.total,
        },
    }
