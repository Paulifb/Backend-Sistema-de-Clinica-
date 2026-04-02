"""CRUD para Tratamiento"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.entities.tratamiento import Tratamiento
from src.entities.historial import Historial


def crear(
    db: Session,
    id_historial: UUID,
    nombre_tratamiento: str,
    dosis: str,
    duracion: int,
    descripcion: Optional[str] = None,
) -> Tratamiento:

    nombre_tratamiento = nombre_tratamiento.strip()
    dosis = dosis.strip()

    if not nombre_tratamiento:
        raise ValueError("El nombre del tratamiento es obligatorio")

    if not dosis:
        raise ValueError("La dosis es obligatoria")

    if duracion <= 0:
        raise ValueError("La duración debe ser mayor a 0")

    if not db.query(Historial).filter(Historial.id_historial == id_historial).first():
        raise ValueError("El historial no existe")

    tratamiento_existente = (
        db.query(Tratamiento)
        .filter(
            Tratamiento.nombre_tratamiento == nombre_tratamiento,
            Tratamiento.id_historial == id_historial,
        )
        .first()
    )

    if tratamiento_existente:
        raise ValueError("Este tratamiento ya existe en el historial")

    tratamiento = Tratamiento(
        id_historial=id_historial,
        nombre_tratamiento=nombre_tratamiento,
        dosis=dosis,
        duracion=duracion,
        descripcion=descripcion.strip() if descripcion else None,
    )

    db.add(tratamiento)
    db.commit()
    db.refresh(tratamiento)

    return tratamiento


def obtener_por_id(db: Session, id_tratamiento: UUID) -> Optional[Tratamiento]:
    return (
        db.query(Tratamiento)
        .filter(Tratamiento.id_tratamiento == id_tratamiento)
        .first()
    )


def obtener_todos(db: Session) -> List[Tratamiento]:
    return db.query(Tratamiento).all()


def actualizar(
    db: Session,
    id_tratamiento: UUID,
    **kwargs,
) -> Optional[Tratamiento]:

    tratamiento = obtener_por_id(db, id_tratamiento)
    if not tratamiento:
        return None

    for key, value in kwargs.items():

        if isinstance(value, str):
            value = value.strip()

        if key == "nombre_tratamiento" and not value:
            raise ValueError("El nombre del tratamiento es obligatorio")

        if key == "dosis" and not value:
            raise ValueError("La dosis es obligatoria")

        if key == "duracion" and value <= 0:
            raise ValueError("La duración debe ser mayor a 0")

        if key == "id_historial":
            if not db.query(Historial).filter(Historial.id_historial == value).first():
                raise ValueError("El historial no existe")

        setattr(tratamiento, key, value)

    db.commit()
    db.refresh(tratamiento)

    return tratamiento


def eliminar(db: Session, id_tratamiento: UUID) -> bool:

    tratamiento = obtener_por_id(db, id_tratamiento)
    if not tratamiento:
        return False

    db.delete(tratamiento)
    db.commit()

    return True
