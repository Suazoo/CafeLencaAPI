from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.Mesa import Mesa
from app.models.MetodoPago import MetodoPago
from app.models.Empleado import Empleado
from app.models.Persona import Persona
from app.motor_logico.reglas import ESTADOS_ACTIVOS
from app.schemas.CatalogoSchema import MesaResponse, MetodoPagoResponse

router = APIRouter(prefix="/catalogos", tags=["Catálogos"])

@router.get("/mesas", response_model=list[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).filter(Mesa.estado.in_(tuple(ESTADOS_ACTIVOS))).order_by(Mesa.numero).all()

@router.get("/metodos-pago", response_model=list[MetodoPagoResponse])
def listar_metodos_pago(db: Session = Depends(get_db)):
    return db.query(MetodoPago).filter(MetodoPago.estado.in_(tuple(ESTADOS_ACTIVOS))).order_by(MetodoPago.nombre).all()

@router.get("/empleados")
def listar_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleado).join(Persona).order_by(Empleado.idEmpleado).all()
    return [{
        "idEmpleado": e.idEmpleado,
        "Persona_idPersona": e.Persona_idPersona,
        "Pnombre": e.persona.Pnombre,
        "Papellido": e.persona.Papellido,
        "correo": e.persona.correo,
    } for e in empleados]
