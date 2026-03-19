"""CRUD para Médico"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.medico import Medico
from src.entities.usuario import Usuario
from src.entities.especialidad import Especialidad

db = SessionLocal()


def crear_medico(
    nombre: str,
    id_usuario: UUID,
    id_especialidad: UUID,
    telefono: Optional[str] = None,
) -> Medico:
    """
    Registra un nuevo médico en el sistema.
    """
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre del médico no puede estar vacío")

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("El ID de usuario especificado no existe")

    if not db.query(Especialidad).get(id_especialidad):
        raise ValueError("El ID de especialidad especificado no existe")

    nuevo_medico = Medico(
        nombre=nombre,
        id_usuario=id_usuario,  # Este es el único usuario relacionado
        id_especialidad=id_especialidad,
        telefono=telefono,
    )

    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico


def obtener_todos_medicos() -> List[Medico]:
    """Obtiene la lista de todos los médicos registrados."""
    return db.query(Medico).all()


def obtener_medico_por_id(id_medico: UUID) -> Optional[Medico]:
    """Obtiene un médico por su identificador único."""
    return db.query(Medico).filter(Medico.id_medico == id_medico).first()


def actualizar_medico(
    id_medico: UUID,
    id_usuario: UUID,
    **kwargs: dict,
) -> Optional[Medico]:
    """
    Actualiza los campos de un médico existente siguiendo la estructura de trazabilidad.
    """
    medico = obtener_medico_por_id(id_medico)

    if medico is None:
        return None

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario que realiza la edición no existe")

    campos_validos = {"nombre", "telefono", "id_especialidad"}

    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if isinstance(value, str):
            value = value.strip()

        if key == "nombre" and not value:
            raise ValueError("El nombre del médico no puede estar vacío")

        if key == "id_especialidad":
            if not db.query(Especialidad).get(value):
                raise ValueError("La nueva especialidad especificada no existe")

        setattr(medico, key, value)

    medico.id_usuario = id_usuario

    db.commit()
    db.refresh(medico)

    return medico


def eliminar_medico(id_medico: UUID) -> bool:
    """
    Elimina un médico por su identificador.
    """
    medico = obtener_medico_por_id(id_medico)

    if medico:
        db.delete(medico)
        db.commit()
        return True

    return False
