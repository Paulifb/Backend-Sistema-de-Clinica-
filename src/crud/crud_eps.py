"""CRUD para Eps"""

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
