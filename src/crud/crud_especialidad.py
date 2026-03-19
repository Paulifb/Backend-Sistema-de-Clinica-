"""CRUD para Especialidad"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.especialidad import Especialidad
from src.entities.usuario import Usuario

db = SessionLocal()


def crear_especialidad(
    nombre: str, id_usuario: UUID, descripcion: Optional[str] = None
) -> Especialidad:
    """Crea una especialidad normalizando el nombre y validando el usuario."""
    nombre = nombre.strip().capitalize()

    if not nombre:
        raise ValueError("El nombre de la especialidad no puede estar vacío")

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("El usuario especificado no existe")

    nueva = Especialidad(
        nombre=nombre, descripcion=descripcion, id_usuario_creacion=id_usuario
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def obtener_por_id(id_especialidad: UUID) -> Optional[Especialidad]:
    """Busca una especialidad por su ID."""
    return db.query(Especialidad).get(id_especialidad)


def obtener_todas() -> List[Especialidad]:
    """Lista todas las especialidades."""
    return db.query(Especialidad).all()


def actualizar_especialidad(
    id_especialidad: UUID, id_usuario: UUID, **kwargs
) -> Optional[Especialidad]:
    """Actualiza dinámicamente los campos de la especialidad."""
    especialidad = obtener_por_id(id_especialidad)
    if not especialidad:
        return None

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("El usuario especificado no existe")

    campos_validos = {"nombre", "descripcion"}
    for key, value in kwargs.items():
        if key in campos_validos:
            if key == "nombre":
                value = value.strip().capitalize()
                if not value:
                    raise ValueError("El nombre no puede estar vacío")
            setattr(especialidad, key, value)

    especialidad.id_usuario_edita = id_usuario
    db.commit()
    db.refresh(especialidad)
    return especialidad


def eliminar_especialidad(id_especialidad: UUID) -> bool:
    """Elimina la especialidad si existe."""
    especialidad = obtener_por_id(id_especialidad)
    if especialidad:
        db.delete(especialidad)
        db.commit()
        return True
    return False
