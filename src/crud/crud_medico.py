"""CRUD para Médico (con trazabilidad)"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.medico import Medico

db = SessionLocal()


def crear_medico(
    id_usuario: UUID,
    id_especialidad: UUID,
    nombre: str,
    telefono: Optional[str] = None,
    registro_medico: Optional[str] = None,
) -> Medico:
    """
    Registra un nuevo médico en el sistema.
    """
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")

    nuevo_medico = Medico(
        id_usuario=id_usuario,
        id_especialidad=id_especialidad,
        nombre=nombre,
        telefono=telefono,
        registro_medico=registro_medico,
    )

    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico


def obtener_medico_por_id(id_medico: UUID) -> Optional[Medico]:
    """Obtiene un médico por su identificador único."""
    return db.query(Medico).filter(Medico.id_medico == id_medico).first()
