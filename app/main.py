import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.clientes import router as clientes_router
from app.routers.productos import router as productos_router
from app.routers.categorias import router as categorias_router
from app.routers.catalogos import router as catalogos_router
from app.routers.pedidos import router as pedidos_router
from app.routers.reservas import router as reservas_router
from app.routers.dashboard import router as dashboard_router
from app.routers.motor_logico import router as motor_logico_router
from app.routers.reportes import router as reportes_router
from app.routers.inventario import router as inventario_router
from app.routers.health import router as health_router

app = FastAPI(
    title="Café Lenca API",
    description=(
        "API para gestionar clientes, catálogo, pedidos, facturas e inventario. "
        "Incluye ejemplos académicos de cinco paradigmas de programación."
    ),
    version="1.0.0",
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,https://cafe-lenca.vercel.app",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "message": "Café Lenca API está en funcionamiento.",
        "docs": "/docs",
        "health": "/health",
    }

for router in (
    health_router, clientes_router, productos_router, categorias_router,
    catalogos_router, pedidos_router, reservas_router, dashboard_router,
    motor_logico_router, reportes_router, inventario_router,
):
    app.include_router(router)
