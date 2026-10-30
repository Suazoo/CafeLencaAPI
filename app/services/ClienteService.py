from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from app.models.Cliente import Cliente
from app.models.Persona import Persona
from app.models.Telefono import Telefono
from app.paradigmas.funcional import normalizar_texto

class ClienteService:
    @staticmethod
    def obtener_clientes(db: Session):
        return db.query(Cliente).options(joinedload(Cliente.persona)).order_by(Cliente.idCliente).all()

    @staticmethod
    def obtener_cliente(db: Session, cliente_id: int):
        return db.query(Cliente).options(joinedload(Cliente.persona)).filter(Cliente.idCliente == cliente_id).first()

    @staticmethod
    def crear_cliente(db: Session, datos: dict):
        try:
            persona = Persona(
                Pnombre=normalizar_texto(datos["Pnombre"]),
                Snombre=normalizar_texto(datos.get("Snombre")) or None,
                Papellido=normalizar_texto(datos["Papellido"]),
                Sapellido=normalizar_texto(datos.get("Sapellido")) or None,
                correo=str(datos["correo"]).strip().lower(),
                Fecha_registro=datetime.now(timezone.utc).replace(tzinfo=None),
            )
            db.add(persona)
            db.flush()
            cliente = Cliente(Persona_idPersona=persona.idPersona, persona=persona)
            db.add(cliente)
            db.flush()
            if datos.get("telefono"):
                db.add(Telefono(numero=datos["telefono"].strip(), Persona_idPersona=persona.idPersona))
            db.commit()
            db.refresh(cliente)
            return ClienteService.obtener_cliente(db, cliente.idCliente)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id: int, datos: dict):
        cliente = ClienteService.obtener_cliente(db, cliente_id)
        if not cliente:
            return None
        try:
            persona = cliente.persona
            for campo in ("Pnombre", "Snombre", "Papellido", "Sapellido"):
                if campo in datos and datos[campo] is not None:
                    valor = normalizar_texto(datos[campo])
                    setattr(persona, campo, valor or None)
            if datos.get("correo") is not None:
                persona.correo = str(datos["correo"]).strip().lower()
            if datos.get("telefono") is not None:
                telefono = db.query(Telefono).filter(Telefono.Persona_idPersona == persona.idPersona).first()
                if telefono:
                    telefono.numero = datos["telefono"].strip()
                elif datos["telefono"].strip():
                    db.add(Telefono(numero=datos["telefono"].strip(), Persona_idPersona=persona.idPersona))
            db.commit()
            return ClienteService.obtener_cliente(db, cliente_id)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def eliminar_cliente(db: Session, cliente_id: int):
        cliente = ClienteService.obtener_cliente(db, cliente_id)
        if not cliente:
            return False
        # Borrar Persona elimina Cliente por FK ON DELETE CASCADE en el esquema.
        db.delete(cliente.persona)
        db.commit()
        return True
