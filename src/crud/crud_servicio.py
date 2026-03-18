"""CRUD para Servicio (con trazabilidad)"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.servicio import Servicio

db = SessionLocal()


def crear_servicio(
    nombre: str,
    costo_base: float,
    descripcion: Optional[str] = None,
    duracion_aproximada: Optional[str] = None,
) -> Servicio:
    """
    Crea un nuevo servicio médico en el catálogo.
    """
    if costo_base < 0:
        raise ValueError("El costo no puede ser negativo")

    nuevo_servicio = Servicio(
        nombre=nombre.strip(),
        costo_base=costo_base,
        descripcion=descripcion,
        duracion_aproximada=duracion_aproximada,
    )

    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio
