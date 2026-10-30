"""Caso de uso transaccional para registrar pedidos y facturas."""
import os
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from app.models.Pedido import Pedido
from app.models.DetallePedido import DetallePedido
from app.models.Factura import Factura
from app.models.Producto import Producto
from app.models.Cliente import Cliente
from app.models.Mesa import Mesa
from app.models.MetodoPago import MetodoPago
from app.models.Empleado import Empleado
from app.motor_logico.reglas import validar_producto_vendible, validar_y_descontar_receta
from app.paradigmas.funcional import calcular_totales, dinero
from app.paradigmas.orientado_objetos import PoliticaPedido

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
        politica = PoliticaPedido()
        lineas = []
        subtotal = Decimal("0.00")
        alertas = []
        try:
            # Validar referencias opcionales antes de crear el pedido.
            referencias = [
                ("Cliente_idCliente", Cliente, "El cliente no existe."),
                ("Mesa_idMesa", Mesa, "La mesa no existe."),
                ("MetodoPago_idMetodoPago", MetodoPago, "El método de pago no existe."),
                ("Empleado_idEmpleado", Empleado, "El empleado no existe."),
            ]
            for campo, modelo, mensaje in referencias:
                valor = datos.get(campo)
                if valor is not None and db.get(modelo, valor) is None:
                    raise ValueError(mensaje)

            for linea in datos["detalles"]:
                cantidad = int(linea["cantidad"])
                politica.validar_cantidad(cantidad)
                producto = (
                    db.query(Producto)
                    .filter(Producto.idProducto == linea["Producto_idProducto"])
                    .with_for_update()
                    .first()
                )
                if not producto:
                    raise ValueError(f"No existe el producto {linea['Producto_idProducto']}.")
                validar_producto_vendible(producto, cantidad)
                precio = dinero(producto.precio)
                subtotal += precio * cantidad
                lineas.append((producto, cantidad, precio))

            subtotal = dinero(subtotal)
            descuento = dinero(datos.get("descuento", 0))
            politica.validar_descuento(descuento, subtotal)
            try:
                tasa = Decimal(os.getenv("TAX_RATE", "0.15"))
            except Exception:
                tasa = Decimal("0.15")
            if tasa < 0 or tasa > 1:
                raise ValueError("TAX_RATE debe estar entre 0 y 1.")

            totales = calcular_totales(subtotal, descuento, tasa)
            pedido = Pedido(
                Cliente_idCliente=datos.get("Cliente_idCliente"),
                Mesa_idMesa=datos.get("Mesa_idMesa"),
                MetodoPago_idMetodoPago=datos.get("MetodoPago_idMetodoPago"),
                Empleado_idEmpleado=datos.get("Empleado_idEmpleado"),
                estado="1",
                fecha_pedido=datetime.now(timezone.utc).replace(tzinfo=None),
            )
            db.add(pedido)
            db.flush()

            for producto, cantidad, precio in lineas:
                alertas.extend(validar_y_descontar_receta(db, producto.idProducto, cantidad))
                db.add(DetallePedido(
                    Producto_idProducto=producto.idProducto,
                    Pedido_idPedido=pedido.idPedido,
                    cantidad=cantidad,
                    precio_unitario=precio,
                ))

            factura = Factura(
                numero_factura=f"CL-{datetime.now().strftime('%Y%m%d')}-{pedido.idPedido:06d}",
                fecha_emision=datetime.now(timezone.utc).replace(tzinfo=None),
                subtotal=totales["subtotal"],
                descuento=totales["descuento"],
                impuesto=totales["impuesto"],
                total=totales["total"],
                Pedido_idPedido=pedido.idPedido,
            )
            db.add(factura)
            db.commit()
            pedido = PedidoService.obtener_por_id(db, pedido.idPedido)
            return {"pedido": pedido, "alertas_inventario": alertas}
        except Exception:
            db.rollback()
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
