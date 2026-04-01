from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.servicio import Servicio
from src.entities.usuario import Usuario


def crear_servicio(
    db: Session,
    nombre: str,
    costo_base: float,
    id_usuario: UUID,
    descripcion: Optional[str] = None,
    duracion_aproximada: Optional[str] = None,
) -> Servicio:
    """
    Registra un servicio médico con su costo base.

    Args:
        db: Sesión de SQLAlchemy.
        nombre: Nombre del servicio.
        costo_base: Precio del servicio (debe ser > 0).
        id_usuario: Usuario responsable.
        descripcion: Descripción opcional.
        duracion_aproximada: Tiempo estimado.
    """
    if costo_base <= 0:
        raise ValueError("El costo debe ser mayor a cero")

    nuevo = Servicio(
        nombre=nombre.strip(),
        costo_base=costo_base,
        descripcion=descripcion,
        duracion_aproximada=duracion_aproximada,
        id_usuario=id_usuario,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
