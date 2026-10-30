from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ClienteSchema import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services.ClienteService import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    return ClienteService.obtener_clientes(db)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = ClienteService.obtener_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return cliente

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    try:
        return ClienteService.crear_cliente(db, datos.model_dump())
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo registrar el cliente. Verifica que el correo no esté registrado.") from exc

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    try:
        cliente = ClienteService.actualizar_cliente(db, cliente_id, datos.model_dump(exclude_unset=True))
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
        return cliente
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="El correo ya está registrado por otra persona.") from exc

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        if not ClienteService.eliminar_cliente(db, cliente_id):
            raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se puede eliminar el cliente porque tiene registros relacionados.") from exc
