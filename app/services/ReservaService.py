from sqlalchemy.orm import Session
from app.models.Reserva import Reserva
from app.models.Cliente import Cliente
from app.models.Mesa import Mesa
from app.motor_logico.reglas import ESTADOS_ACTIVOS

class ReservaService:
    @staticmethod
    def listar(db: Session):
        return db.query(Reserva).order_by(Reserva.fecha_reserva.desc()).all()

    @staticmethod
    def crear(db: Session, datos: dict):
        cliente = db.get(Cliente, datos["Cliente_idCliente"])
        if not cliente:
            raise ValueError("El cliente indicado no existe.")
        mesa_id = datos.get("Mesa_idMesa")
        if mesa_id is not None:
            mesa = db.get(Mesa, mesa_id)
            if not mesa:
                raise ValueError("La mesa indicada no existe.")
            if str(mesa.estado).strip() not in ESTADOS_ACTIVOS:
                raise ValueError("La mesa no está activa.")
            if mesa.capacidad < datos["cantidad_persona"]:
                raise ValueError("La mesa no tiene capacidad suficiente.")
            conflicto = db.query(Reserva).filter(
                Reserva.Mesa_idMesa == mesa_id,
                Reserva.fecha_reserva == datos["fecha_reserva"],
                Reserva.estado.in_(tuple(ESTADOS_ACTIVOS)),
            ).first()
            if conflicto:
                raise ValueError("La mesa ya tiene una reserva para esa fecha y hora.")
        reserva = Reserva(**datos)
        db.add(reserva)
        try:
            db.commit()
            db.refresh(reserva)
            return reserva
        except Exception:
            db.rollback()
            raise
