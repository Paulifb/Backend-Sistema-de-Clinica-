"""CRUD para Especialidad (con trazabilidad)"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.especialidad import Especialidad

db = SessionLocal()


def crear_especialidad(nombre: str, descripcion: Optional[str] = None) -> Especialidad:
    """
    Registra una nueva especialidad médica.
    """
    nueva_especialidad = Especialidad(nombre=nombre.strip(), descripcion=descripcion)

    db.add(nueva_especialidad)
    db.commit()
    db.refresh(nueva_especialidad)
    return nueva_especialidad
