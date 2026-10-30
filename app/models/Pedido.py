from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Pedido(Base):
    __tablename__ = "pedido"
    idPedido: Mapped[int] = mapped_column("idpedido", primary_key=True)
    fecha_pedido: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    estado: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'1'"))
    Cliente_idCliente: Mapped[int | None] = mapped_column(
        "cliente_idcliente", ForeignKey("cliente.idcliente", ondelete="SET NULL"), nullable=True
    )
    Mesa_idMesa: Mapped[int | None] = mapped_column(
        "mesa_idmesa", ForeignKey("mesa.idmesa", ondelete="SET NULL"), nullable=True
    )
    MetodoPago_idMetodoPago: Mapped[int | None] = mapped_column(
        "metodopago_idmetodopago", ForeignKey("metodopago.idmetodopago", ondelete="SET NULL"), nullable=True
    )
    Empleado_idEmpleado: Mapped[int | None] = mapped_column(
        "empleado_idempleado", ForeignKey("empleado.idempleado", ondelete="SET NULL"), nullable=True
    )
    cliente = relationship("Cliente", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    metodo_pago = relationship("MetodoPago", back_populates="pedidos")
    empleado = relationship("Empleado", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="pedido", uselist=False, cascade="all, delete-orphan")
