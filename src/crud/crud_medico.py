from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.medico import Medico
from src.entities.usuario import Usuario
from src.entities.especialidad import Especialidad


def crear_medico(
    db: Session,
    nombre: str,
    id_usuario: UUID,
    id_especialidad: UUID,
    telefono: Optional[str] = None,
) -> Medico:
    """
    Registra un nuevo médico en el sistema validando dependencias.

    Args:
        db: Sesión activa de la base de datos.
        nombre: Nombre completo del médico.
        id_usuario: Identificador del usuario creador.
        id_especialidad: Identificador de la especialidad asociada.
        telefono: Número telefónico opcional.

    Returns:
        El objeto Medico creado tras el commit.
    """
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El nombre del médico no puede estar vacío")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El ID de usuario especificado no existe")

    if (
        not db.query(Especialidad)
        .filter(Especialidad.id_especialidad == id_especialidad)
        .first()
    ):
        raise ValueError("El ID de especialidad especificado no existe")

    nuevo_medico = Medico(
        nombre=nombre,
        id_usuario=id_usuario,
        id_especialidad=id_especialidad,
        telefono=telefono,
    )

    db.add(nuevo_medico)
    db.commit()
    db.refresh(nuevo_medico)
    return nuevo_medico


def obtener_todos_medicos(db: Session) -> List[Medico]:
    """Obtiene la lista de todos los médicos registrados."""
    return db.query(Medico).all()


def obtener_medico_por_id(db: Session, id_medico: UUID) -> Optional[Medico]:
    """Busca un médico específico por su UUID."""
    return db.query(Medico).filter(Medico.id_medico == id_medico).first()


def eliminar_medico(db: Session, id_medico: UUID) -> bool:
    """Elimina el registro de un médico si existe."""
    medico = obtener_medico_por_id(db, id_medico)
    if medico:
        db.delete(medico)
        db.commit()
        return True
    return False
