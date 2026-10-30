from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.models.Categoria import Categoria
from app.schemas.CatalogoSchema import CategoriaCreate, CategoriaResponse
from app.paradigmas.declarativo import categorias_activas

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return categorias_activas(db)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = Categoria(**datos.model_dump())
    db.add(categoria)
    try:
        db.commit()
        db.refresh(categoria)
        return categoria
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo registrar la categoría.") from exc
