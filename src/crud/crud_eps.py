"""CRUD para Eps"""

from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.eps import Eps

db = SessionLocal()


def crear_eps(
    nombre: str,
    telefono: str,
    direccion: str,
    id_usuario_creacion: UUID,
    correo: Optional[str] = None,
    ciudad: Optional[str] = None,
) -> Eps:

    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")

    if not telefono.strip():
        raise ValueError("El teléfono es obligatorio")

    if not direccion.strip():
        raise ValueError("La dirección es obligatoria")

    # Validar duplicado
    eps_existente = db.query(Eps).filter(Eps.nombre == nombre.strip()).first()

    if eps_existente:
        raise ValueError("La EPS ya existe")

    eps = Eps(
        nombre=nombre.strip(),
        telefono=telefono.strip(),
        direccion=direccion.strip(),
        correo=correo.strip() if correo else None,
        ciudad=ciudad.strip() if ciudad else None,
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(eps)
    db.commit()
    db.refresh(eps)

    return eps


def obtener_por_id(id_eps: UUID) -> Optional[Eps]:
    return db.query(Eps).filter(Eps.id_eps == id_eps).first()


def obtener_todos() -> List[Eps]:
    return db.query(Eps).all()


def actualizar(
    id_eps: UUID,
    id_usuario_edita: UUID,
    **kwargs,
) -> Optional[Eps]:

    eps = obtener_por_id(id_eps)

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


def eliminar(id_eps: UUID) -> bool:

    eps = obtener_por_id(id_eps)

    if not eps:
        return False

    db.delete(eps)
    db.commit()

    return True
