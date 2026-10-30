from sqlalchemy.orm import Session
from datetime import datetime
from app.models.Cliente import Cliente
from app.models.Persona import Persona


class ClienteRepository:

    @staticmethod
    def obtener_todos(db: Session):
        return (
            db.query(Cliente)
            .join(Persona)
            .all()
        )

    @staticmethod
    def obtener_por_id(db: Session, cliente_id: int):
        return (
            db.query(Cliente)
            .join(Persona)
            .filter(Cliente.idCliente == cliente_id)
            .first()
        )

    @staticmethod
    def crear(db: Session, datos: dict):
        persona = Persona(
            Pnombre=datos["Pnombre"],
            Snombre=datos.get("Snombre"),
            Papellido=datos["Papellido"],
            Sapellido=datos.get("Sapellido"),
            correo=datos.get("correo"),
            Fecha_registro=datetime.now()
        )

        db.add(persona)
        db.flush()

        cliente = Cliente(
            Persona_idPersona=persona.idPersona
        )

        db.add(cliente)
        db.flush()
        db.refresh(cliente)

        return cliente
