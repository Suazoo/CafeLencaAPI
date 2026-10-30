from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ReservaSchema import ReservaCreate, ReservaResponse
from app.services.ReservaService import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService.listar(db)

@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(datos: ReservaCreate, db: Session = Depends(get_db)):
    try:
        return ReservaService.crear(db, datos.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo registrar la reserva.") from exc
