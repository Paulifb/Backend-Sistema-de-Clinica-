"""CRUD para la entidad EPS."""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.eps import Eps


def crear_eps(
    db: Session,
    nombre: str,
    telefono: str,
    direccion: str,
    correo: Optional[str] = None,
    ciudad: Optional[str] = None,
) -> Eps:
    """
    Crea un registro de EPS.

    Valida campos obligatorios y evita duplicados.
    """

    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    if not telefono.strip():
        raise ValueError("El teléfono es obligatorio")

    if not direccion.strip():
        raise ValueError("La dirección es obligatoria")

    eps_existente = db.query(Eps).filter(Eps.nombre == nombre.strip()).first()
    if eps_existente:
        raise ValueError("La EPS ya existe")

    eps = Eps(
        nombre=nombre.strip(),
        telefono=telefono.strip(),
        direccion=direccion.strip(),
        correo=correo.strip() if correo else None,
        ciudad=ciudad.strip() if ciudad else None,
    )

    db.add(eps)
    db.commit()
    db.refresh(eps)
    return eps


def obtener_por_id(db: Session, id_eps: UUID) -> Optional[Eps]:
    """
    Obtiene una EPS por ID.
    """
    return db.query(Eps).filter(Eps.id_eps == id_eps).first()


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Eps]:
    """
    Lista todas las EPS registradas.
    """
    return db.query(Eps).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_eps: UUID,
    id_usuario_edita: UUID,
    **kwargs,
) -> Optional[Eps]:
    """
    Actualiza los datos de una EPS.
    """

    eps = obtener_por_id(db, id_eps)
    if not eps:
        return None

    for key, value in kwargs.items():
        if isinstance(value, str):
            value = value.strip()
        setattr(eps, key, value)

    eps.id_usuario_edita = id_usuario_edita

    db.commit()
    db.refresh(eps)
    return eps


def eliminar(db: Session, id_eps: UUID) -> bool:
    """
    Elimina una EPS por ID.
    """

    eps = obtener_por_id(db, id_eps)
    if not eps:
        return False

    db.delete(eps)
    db.commit()
    return True
