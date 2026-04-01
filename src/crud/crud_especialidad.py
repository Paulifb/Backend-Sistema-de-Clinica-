from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.especialidad import Especialidad
from src.entities.usuario import Usuario


def crear_especialidad(
    db: Session, nombre: str, id_usuario: UUID, descripcion: Optional[str] = None
) -> Especialidad:
    """
    Crea una especialidad médica normalizando el texto.

    Args:
        db: Sesión de base de datos.
        nombre: Nombre de la especialidad.
        id_usuario: ID del usuario administrador.
        descripcion: Detalle opcional de la especialidad.
    """
    nombre = nombre.strip().capitalize()
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    nueva = Especialidad(nombre=nombre, descripcion=descripcion, id_usuario=id_usuario)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_por_id(db: Session, id_especialidad: UUID) -> Optional[Especialidad]:
    """Busca especialidad por identificador único."""
    return (
        db.query(Especialidad)
        .filter(Especialidad.id_especialidad == id_especialidad)
        .first()
    )


def obtener_todas(db: Session) -> List[Especialidad]:
    """Retorna todas las especialidades disponibles."""
    return db.query(Especialidad).all()
