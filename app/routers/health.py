from fastapi import APIRouter
from sqlalchemy import text
from app.core.database import engine

router = APIRouter(tags=["Estado del servicio"])

@router.get("/health")
def health():
    return {"status": "ok", "service": "cafe-lenca-api"}

@router.get("/health/db")
def health_db():
    if engine is None:
        return {"status": "error", "database": "DATABASE_URL no configurada"}
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        # No se exponen credenciales ni detalles internos al cliente.
        return {"status": "error", "database": "connection_failed", "detail": str(exc).splitlines()[0][:250]}
