"""CRUD para Enfermero"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.enfermero import Enfermero
from src.entities.usuario import Usuario


def crear_enfermero(
    db: Session,
    nombre: str,
    telefono: str,
    area: str,
    turno: str,
    id_usuario: UUID,
) -> Enfermero:
    """
    Crea un nuevo registro de enfermero en el sistema.

    Args:
        nombre: Nombre completo del enfermero.
        telefono: Número de teléfono del enfermero.
        area: Área de trabajo del enfermero.
        turno: Turno asignado al enfermero.
        id_usuario: Usuario que crea el registro del enfermero.
    Returns:
        El registro del enfermero creado.
    """

    nombre = nombre.strip()
    telefono = telefono.strip()
    area = area.strip().lower()
    turno = turno.strip().lower()

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    if not nombre:
        raise ValueError("El nombre del enfermero no puede estar vacío")

    if not telefono:
        raise ValueError("El teléfono del enfermero no puede estar vacío")

    areas_validas = ["pediatria", "geriatria", "urgencias", "cuidados intensivos"]

    if area not in areas_validas:
        raise ValueError("El área de trabajo del enfermero no es válida")

    turnos_validos = ["mañana", "tarde", "noche"]

    if turno not in turnos_validos:
        raise ValueError("El turno del enfermero debe ser 'mañana', 'tarde' o 'noche'")

    enfermero = Enfermero(
        nombre=nombre,
        telefono=telefono,
        area=area,
        turno=turno,
        id_usuario=id_usuario,
    )
    db.add(enfermero)
    db.commit()
    db.refresh(enfermero)

    return enfermero


def obtener_por_id(db: Session, id_enfermero: UUID) -> Optional[Enfermero]:
    """
    Obtiene un registro del enfermero por su identificador.
    """

    return db.query(Enfermero).filter(Enfermero.id_enfermero == id_enfermero).first()


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Enfermero]:
    """
    Obtiene todos los registros del enfermero con paginación.
    """

    return db.query(Enfermero).offset(skip).limit(limit).all()


def actualizar_enfermero(
    db: Session,
    id_enfermero: UUID,
    id_usuario: UUID,
    **kwargs: dict,
) -> Optional[Enfermero]:
    """
    Actualiza los campos de un registro del enfermero.

    Permite modificar dinámicamente los atributos del enfermero a partir de
    un diccionario con los valores a actualizar.

    Args:
        id_enfermero: Identificador del registro del enfermero a actualizar.
        id_usuario: Usuario que realiza la modificación.
        args: Diccionario con los campos y valores a actualizar.

    Returns:
        El registro del enfermero actualizado o None si no existe.
    """

    enfermero = obtener_por_id(db, id_enfermero)

    if enfermero is None:
        return None

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    campos_validos = {"nombre", "telefono", "area", "turno"}

    areas_validas = ["pediatria", "geriatria", "urgencias", "cuidados intensivos"]
    turnos_validos = ["mañana", "tarde", "noche"]

    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if isinstance(value, str):
            value = value.strip()

        if key == "area":
            value = value.lower()
            if value not in areas_validas:
                raise ValueError("El area de trabajo del enfermero no es valida")

        if key == "turno":
            value = value.lower()
            if value not in turnos_validos:
                raise ValueError("El turno del enfermero no es valido")

        setattr(enfermero, key, value)

    enfermero.id_usuario = id_usuario

    db.commit()
    db.refresh(enfermero)

    return enfermero


def eliminar_enfermero(db: Session, id_enfermero: UUID) -> bool:
    """
    Elimina un registro del enfermero por su identificador.
    """

    enfermero = obtener_por_id(db, id_enfermero)

    if enfermero:
        db.delete(enfermero)
        db.commit()
        return True

    return False
