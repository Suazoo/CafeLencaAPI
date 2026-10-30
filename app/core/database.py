"""Configuración central de SQLAlchemy y conexión segura a PostgreSQL/Supabase."""
import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)


if DATABASE_URL.startswith("postgresql+psycopg://"):
    parsed = urlsplit(DATABASE_URL)
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
             if k.lower() != "pgbouncer"]
    if not any(k.lower() == "sslmode" for k, _ in query):
        query.append(("sslmode", "require"))
    DATABASE_URL = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))

engine = None
if DATABASE_URL:
    
    opciones = {"pool_pre_ping": True, "pool_recycle": 300}
    if DATABASE_URL.startswith("postgresql+psycopg://"):
        opciones["connect_args"] = {"prepare_threshold": None}
    engine = create_engine(DATABASE_URL, **opciones)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)
Base = declarative_base()


def get_db():
    """Dependencia FastAPI: una sesión por petición."""
    if engine is None:
        raise RuntimeError(
            "Falta DATABASE_URL. Crea el archivo .env a partir de .env.example."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
