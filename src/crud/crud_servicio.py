from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.servicio import Servicio
from src.entities.usuario import Usuario


def obtener_servicio_por_id(db: Session, id_servicio: UUID) -> Optional[Servicio]:
    """Busca un servicio específico por su ID."""
    return db.query(Servicio).filter(Servicio.id_servicio == id_servicio).first()


def obtener_todos_servicios(db: Session) -> List[Servicio]:
    """Obtiene la lista de todos los servicios ofrecidos por la clínica."""
    return db.query(Servicio).all()


def crear_servicio(
    db: Session,
    nombre: str,
    costo_base: float,
    id_usuario: UUID,
    descripcion: Optional[str] = None,
    duracion_aproximada: Optional[str] = None,
) -> Servicio:
    """Crea un nuevo servicio validando que el costo sea un valor positivo."""
    if costo_base <= 0:
        raise ValueError("El costo base debe ser mayor a cero")

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


def actualizar_servicio(
    db: Session, id_servicio: UUID, id_usuario: UUID, **kwargs
) -> Optional[Servicio]:
    """Actualiza los campos de un servicio existente (costo, nombre, duración, etc.)."""
    servicio = obtener_servicio_por_id(db, id_servicio)
    if not servicio:
        return None

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("Usuario no encontrado")

    campos_validos = {"nombre", "costo_base", "descripcion", "duracion_aproximada"}
    for key, value in kwargs.items():
        if key in campos_validos:
            if key == "costo_base" and value <= 0:
                raise ValueError("Costo inválido")
            if isinstance(value, str):
                value = value.strip()
            setattr(servicio, key, value)

    servicio.id_usuario = id_usuario
    db.commit()
    db.refresh(servicio)
    return servicio


def eliminar_servicio(db: Session, id_servicio: UUID) -> bool:
    """Elimina un servicio de la clínica tras confirmar su existencia."""
    servicio = obtener_servicio_por_id(db, id_servicio)
    if servicio:
        db.delete(servicio)
        db.commit()
        return True
    return False
