"""CRUD para Servicio"""

from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.servicio import Servicio
from src.entities.usuario import Usuario

db = SessionLocal()


def crear_servicio(
    nombre: str, precio: float, id_usuario: UUID, estado: str = "activo"
) -> Servicio:
    """Registra un servicio validando precio y estado."""
    nombre = nombre.strip()
    estado = estado.strip().lower()

    if not nombre:
        raise ValueError("El nombre del servicio es obligatorio")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a cero")
    if estado not in ["activo", "inactivo"]:
        raise ValueError("El estado debe ser 'activo' o 'inactivo'")

    if not db.query(Usuario).get(id_usuario):
        raise ValueError("Usuario no encontrado")

    nuevo = Servicio(
        nombre=nombre, precio=precio, estado=estado, id_usuario_creacion=id_usuario
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def obtener_por_id(id_servicio: UUID) -> Optional[Servicio]:
    """Obtiene servicio por ID."""
    return db.query(Servicio).get(id_servicio)


def obtener_todos() -> List[Servicio]:
    """Lista todos los servicios."""
    return db.query(Servicio).all()


def actualizar_servicio(
    id_servicio: UUID, id_usuario: UUID, **kwargs
) -> Optional[Servicio]:
    """Actualización dinámica con validación de tipos."""
    servicio = obtener_por_id(id_servicio)
    if not servicio or not db.query(Usuario).get(id_usuario):
        return None

    campos_validos = {"nombre", "precio", "estado"}
    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if key == "precio" and value <= 0:
            raise ValueError("Precio inválido")
        if key == "estado" and value.strip().lower() not in ["activo", "inactivo"]:
            raise ValueError("Estado inválido")

        setattr(servicio, key, value)

    servicio.id_usuario_edita = id_usuario
    db.commit()
    db.refresh(servicio)
    return servicio


def eliminar_servicio(id_servicio: UUID) -> bool:
    """Elimina el servicio de la base de datos."""
    servicio = obtener_por_id(id_servicio)
    if servicio:
        db.delete(servicio)
        db.commit()
        return True
    return False
