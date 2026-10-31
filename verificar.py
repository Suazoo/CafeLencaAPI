"""
Verifica que las tablas y columnas del ORM coincidan con la base de datos.
Ejecutar solo después de configurar .env. Es una verificación de solo lectura.
"""
from sqlalchemy import inspect
from app.core.database import engine, Base
import app.models  # registra todos los modelos

if engine is None:
    raise SystemExit("Falta DATABASE_URL en .env.")

inspector = inspect(engine)
tablas_bd = set(inspector.get_table_names())
tablas_orm = set(Base.metadata.tables.keys())
print("Solo en BD:", sorted(tablas_bd - tablas_orm))
print("Solo en ORM:", sorted(tablas_orm - tablas_bd))

for tabla in sorted(tablas_bd & tablas_orm):
    columnas_bd = {c["name"] for c in inspector.get_columns(tabla)}
    columnas_orm = {c.name for c in Base.metadata.tables[tabla].columns}
    if columnas_bd != columnas_orm:
        print(f"{tabla}: solo BD={sorted(columnas_bd - columnas_orm)}; solo ORM={sorted(columnas_orm - columnas_bd)}")
print("Verificación de solo lectura terminada.")
