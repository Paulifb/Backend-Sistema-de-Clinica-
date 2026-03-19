"""CRUD para Servicio"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.servicio import Servicio
from src.entities.usuario import Usuario

db = SessionLocal()


def crear_servicio(
    nombre: str,
    costo_base: float,
    id_usuario: UUID,
    descripcion: Optional[str] = None,
    duracion_aproximada: Optional[str] = None,
) -> Servicio:
    """Registra un servicio validando costo."""

    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre del servicio es obligatorio")

    if costo_base <= 0:
        raise ValueError("El costo debe ser mayor a cero")

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("Usuario no encontrado")

    nuevo = Servicio(
        nombre=nombre,
        costo_base=costo_base,
        descripcion=descripcion,
        duracion_aproximada=duracion_aproximada,
        id_usuario=id_usuario,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_por_id(id_servicio: UUID) -> Optional[Servicio]:
    return db.query(Servicio).get(id_servicio)


def obtener_todos() -> List[Servicio]:
    return db.query(Servicio).all()


def actualizar_servicio(
    id_servicio: UUID, id_usuario: UUID, **kwargs
) -> Optional[Servicio]:

    servicio = obtener_por_id(id_servicio)

    if not servicio:
        return None

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("Usuario no encontrado")

    campos_validos = {"nombre", "costo_base", "descripcion", "duracion_aproximada"}

    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if key == "costo_base" and value <= 0:
            raise ValueError("Costo inválido")

        if isinstance(value, str):
            value = value.strip()

        setattr(servicio, key, value)

    servicio.id_usuario = id_usuario

    db.commit()
    db.refresh(servicio)
    return servicio


def eliminar_servicio(id_servicio: UUID) -> bool:
    servicio = obtener_por_id(id_servicio)

    if servicio:
        db.delete(servicio)
        db.commit()
        return True

    return False
