from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ProductoSchema import ProductoCreate, ProductoUpdate, ProductoResponse
from app.services.ProductoService import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=list[ProductoResponse])
def obtener_productos(db: Session = Depends(get_db)):
    return ProductoService.obtener_productos(db)

@router.get("/disponibles", response_model=list[ProductoResponse])
def obtener_productos_disponibles(db: Session = Depends(get_db)):
    return ProductoService.obtener_productos_disponibles(db)

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = ProductoService.obtener_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate, db: Session = Depends(get_db)):
    try:
        return ProductoService.crear_producto(db, datos.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo guardar el producto; revisa sus datos y relaciones.") from exc

@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    try:
        producto = ProductoService.actualizar_producto(db, producto_id, datos.model_dump(exclude_unset=True))
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        return producto
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="No se pudo actualizar el producto.") from exc
