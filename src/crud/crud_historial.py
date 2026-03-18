"""CRUD para Historial (con trazabilidad)"""

from typing import List, Optional, Text
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.historial import Historial
from src.entities.cita import Cita
from src.entities.enfermero import Enfermero

db = SessionLocal()


def crear_historial(
    id_cita: UUID,
    id_enfermero: UUID,
    diagnostico: str,
    observaciones_medicas: Text,
    indicaciones_enfermeria: Text,
    observaciones_enfermeria: Text,
    id_usuario_creacion: UUID,
) -> Historial:
    """
    Crea un nuevo registro en el historial.

    Args:
        id_cita: Identificador de la cita asociada al historial.
        id_enfermero: Identificador del enfermero que atiende la cita.
        diagnostico: Diagnóstico médico.
        observaciones_medicas: Observaciones realizadas por el médico.
        indicaciones_enfermeria: Indicaciones para el personal de enfermería.
        observaciones_enfermeria: Observaciones realizadas por el personal de enfermería.
        id_usuario_creacion: Usuario que crea el registro del historial.

    Returns:
        El registro del historial creado.
    """

    if not db.query(Cita).filter(Cita.id_cita == id_cita).first():
        raise ValueError("La cita especificada no existe")

    if not db.query(Enfermero).filter(Enfermero.id_enfermero == id_enfermero).first():
        raise ValueError("El enfermero especificado no existe")

    diagnostico = diagnostico.strip()
    observaciones_medicas = (
        observaciones_medicas.strip() if observaciones_medicas else None
    )
    indicaciones_enfermeria = (
        indicaciones_enfermeria.strip() if indicaciones_enfermeria else None
    )
    observaciones_enfermeria = (
        observaciones_enfermeria.strip() if observaciones_enfermeria else None
    )

    if not diagnostico:
        raise ValueError("El diagnóstico no puede estar vacío")

    if len(diagnostico) > 255:
        raise ValueError("El diagnóstico no puede exceder los 255 caracteres")

    historial = Historial(
        id_cita=id_cita,
        id_enfermero=id_enfermero,
        diagnostico=diagnostico,
        observaciones_medicas=observaciones_medicas,
        indicaciones_enfermeria=indicaciones_enfermeria,
        observaciones_enfermeria=observaciones_enfermeria,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(historial)
    db.commit()
    db.refresh(historial)

    return historial


def obtener_por_id(id_historial: UUID) -> Optional[Historial]:
    """
    Obtiene un registro del historial por su identificador.
    """

    return db.query(Historial).filter(Historial.id_historial == id_historial).first()


def obtener_todos(skip: int = 0, limit: int = 100) -> List[Historial]:
    """
    Obtiene todos los registros del historial con paginación.
    """

    return db.query(Historial).offset(skip).limit(limit).all()


def actualizar_historial(
    id_historial: UUID,
    id_usuario_edicion: UUID,
    **kwargs: dict,
) -> Optional[Historial]:
    """
    Actualiza los campos de un registro del historial.

    Permite modificar dinámicamente los atributos del historial a partir de
    un diccionario con los valores a actualizar.

    Args:
        id_historial: Identificador del registro del historial a actualizar.
        id_usuario_edicion: Usuario que realiza la modificación.
        kwargs: Diccionario con los campos y valores a actualizar.

    Returns:
        El registro del historial actualizado o None si no existe.
    """

    historial = obtener_por_id(id_historial)

    if historial is None:
        return None

    campos_validos = {
        "diagnostico",
        "observaciones_medicas",
        "indicaciones_enfermeria",
        "observaciones_enfermeria",
    }

    if "diagnostico" in kwargs:
        diagnostico = kwargs["diagnostico"]

        if not isinstance(diagnostico, str):
            raise ValueError("El diagnóstico debe ser una cadena de texto")

        diagnostico = diagnostico.strip()

        if not diagnostico:
            raise ValueError("El diagnóstico no puede estar vacío")

        if len(diagnostico) > 255:
            raise ValueError("El diagnóstico no puede exceder los 255 caracteres")

        kwargs["diagnostico"] = diagnostico

    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if isinstance(value, str):
            value = value.strip()

        setattr(historial, key, value)

    historial.id_usuario_edicion = id_usuario_edicion

    db.commit()
    db.refresh(historial)

    return historial


def eliminar_historial(id_historial: UUID) -> bool:
    """
    Elimina un registro del historial por su identificador.
    """

    historial = obtener_por_id(id_historial)

    if historial:
        db.delete(historial)
        db.commit()
        return True

    return False
