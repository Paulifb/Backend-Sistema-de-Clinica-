"""CRUD para Paciente"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from src.database.config import SessionLocal
from src.entities.paciente import Paciente
from src.entities.eps import Eps
from src.entities.usuario import Usuario

db = SessionLocal()


def crear_paciente(
    nombre: str,
    fecha_nacimiento: datetime,
    genero: str,
    tipo_afiliacion: str,
    id_eps: UUID,
    id_usuario: UUID,
    id_usuario_creacion: UUID,
    telefono: Optional[str] = None,
    direccion: Optional[str] = None,
) -> Paciente:

    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    if fecha_nacimiento > datetime.now(timezone.utc):
        raise ValueError("La fecha de nacimiento no puede ser futura")

    if not db.query(Eps).filter(Eps.id_eps == id_eps).first():
        raise ValueError("la Eps no existe")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario no existe")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario_creacion).first():
        raise ValueError("El usuario especificado no existe")

    paciente = Paciente(
        nombre=nombre.strip(),
        telefono=telefono.strip() if telefono else None,
        fecha_nacimiento=fecha_nacimiento,
        direccion=direccion.strip() if direccion else None,
        genero=genero,
        tipo_afiliacion=tipo_afiliacion,
        id_eps=id_eps,
        id_usuario=id_usuario,
    )

    db.add(paciente)
    db.commit()
    db.refresh(paciente)

    return paciente


def obtener_por_id(id_paciente: UUID) -> Optional[Paciente]:
    return db.query(Paciente).filter(Paciente.id_paciente == id_paciente).first()


def obtener_todos() -> List[Paciente]:
    return db.query(Paciente).all()


def actualizar(
    id_paciente: UUID,
    id_usuario_edicion: UUID,
    **kwargs: dict,
) -> Optional[Paciente]:
    paciente = obtener_por_id(id_paciente)

    if not paciente:
        return None
    for key, value in kwargs.items():
        setattr(paciente, key, value)

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario_edicion):
        raise ValueError("El usuario especificado no existe")

    paciente.id_usuario_edicion = id_usuario_edicion
    db.commit()
    db.refresh(paciente)

    return paciente


def eliminar(id_paciente: UUID) -> bool:
    paciente = obtener_por_id(id_paciente)
    if not paciente:
        return False
    db.delete(paciente)
    db.commit()
    return True
