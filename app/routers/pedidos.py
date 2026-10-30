from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.PedidoSchema import PedidoCreate, EstadoPedidoUpdate
from app.services.PedidoService import PedidoService, pedido_a_dict
from app.services.FacturaPdfService import generar_factura_pdf

router = APIRouter(prefix="/pedidos", tags=["Pedidos y facturación"])

@router.get("/")
def listar_pedidos(db: Session = Depends(get_db)):
    return [pedido_a_dict(p) for p in PedidoService.obtener_todos(db)]

@router.get("/{pedido_id}")
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = PedidoService.obtener_por_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")
    return pedido_a_dict(pedido)

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_pedido(datos: PedidoCreate, db: Session = Depends(get_db)):
    try:
        resultado = PedidoService.crear(db, datos.model_dump())
        return {
            **pedido_a_dict(resultado["pedido"]),
            "alertas_inventario": resultado["alertas_inventario"],
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo registrar el pedido por una restricción de la base de datos.") from exc

@router.patch("/{pedido_id}/estado")
def actualizar_estado(pedido_id: int, datos: EstadoPedidoUpdate, db: Session = Depends(get_db)):
    try:
        pedido = PedidoService.actualizar_estado(db, pedido_id, datos.estado)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo actualizar el pedido.") from exc
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")
    return pedido_a_dict(pedido)


@router.get("/{pedido_id}/factura/pdf", response_class=Response)
def descargar_factura_pdf(pedido_id: int, db: Session = Depends(get_db)):
    pedido = PedidoService.obtener_por_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado.")
    if not pedido.factura:
        raise HTTPException(status_code=404, detail="El pedido no tiene factura.")
    try:
        contenido = generar_factura_pdf(pedido)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    nombre = f"factura-{pedido.factura.numero_factura}.pdf"
    return Response(
        content=contenido,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )
