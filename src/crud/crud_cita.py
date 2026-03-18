"""CRUD para Cita (con trazabilidad)"""

import datetime
from datetime import timezone
from typing import List, Optional, Text
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.cita import Cita
from src.entities.paciente import Paciente
from src.entities.servicio import Servicio
from src.entities.medico import Medico

db = SessionLocal()


def crear_cita(
    id_paciente: UUID,
    id_medico: UUID,
    id_servicio: UUID,
    fecha_hora: datetime.datetime,
    motivo: str,
    estado: Text,
    id_usuario_creacion: UUID,
) -> Cita:
    """
    Crea una nueva cita en el sistema.

    Args:
        id_paciente: Identificador del paciente.
        id_medico: Identificador del médico.
        id_servicio: Identificador del servicio.
        fecha_hora: Fecha y hora programada para la cita.
        motivo: Motivo de la consulta.
        estado: Estado inicial de la cita.
        id_usuario_creacion: Usuario que crea la cita.

    Returns:
        La cita creada.
    """

    motivo = motivo.strip()
    estado = estado.strip().lower()

    if not motivo:
        raise ValueError("El motivo de la consulta no puede estar vacío")

    if fecha_hora < datetime.datetime.now(timezone.utc):
        raise ValueError("La fecha y hora de la cita no pueden ser en el pasado")

    estados_validos = ["pendiente", "confirmada", "cancelada"]

    if estado not in estados_validos:
        raise ValueError("El estado de la cita no es válido")

    cita = (
        db.query(Cita)
        .filter(Cita.fecha_hora == fecha_hora, Cita.id_medico == id_medico)
        .first()
    )

    if cita is not None:
        raise ValueError("Ya existe una cita programada para esa fecha y hora")

    if not db.query(Paciente).filter(Paciente.id_paciente == id_paciente).first():
        raise ValueError("El paciente especificado no existe")

    if not db.query(Medico).filter(Medico.id_medico == id_medico).first():
        raise ValueError("El médico especificado no existe")

    if not db.query(Servicio).filter(Servicio.id_servicio == id_servicio).first():
        raise ValueError("El servicio especificado no existe")

    cita = Cita(
        id_paciente=id_paciente,
        id_medico=id_medico,
        id_servicio=id_servicio,
        fecha_hora=fecha_hora,
        motivo=motivo,
        estado=estado,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)

    return cita


def obtener_por_id(id_cita: UUID) -> Optional[Cita]:
    """
    Obtiene una cita por su identificador.
    """

    return db.query(Cita).filter(Cita.id_cita == id_cita).first()


def obtener_todos(skip: int = 0, limit: int = 100) -> List[Cita]:
    """
    Obtiene todas las citas con paginación.
    """

    return db.query(Cita).offset(skip).limit(limit).all()


def actualizar_cita(
    id_cita: UUID,
    id_usuario_edicion: UUID,
    **kwargs: dict,
) -> Optional[Cita]:
    """
    Actualiza los campos de una cita existente.

    Permite modificar dinámicamente los atributos de la cita
    a partir de un diccionario con los valores a actualizar.

    Args:
        id_cita: Identificador de la cita a actualizar.
        id_usuario_edicion: Usuario que realiza la modificación.
        **kwargs: Diccionario con los campos y valores a actualizar.

    Returns:
        La cita actualizada o None si la cita no existe.
    """

    cita = obtener_por_id(id_cita)

    if cita is None:
        return None

    campos_validos = {"fecha_hora", "motivo", "estado"}
    estados_validos = {"pendiente", "confirmada", "cancelada"}

    for key, value in kwargs.items():
        if key not in campos_validos:
            continue

        if isinstance(value, str):
            value = value.strip()

        if key == "estado":
            value = value.lower()
            if value not in estados_validos:
                raise ValueError("El estado de la cita no es válido")

        if key == "motivo" and not value:
            raise ValueError("El motivo de la consulta no puede estar vacío")

        if key == "fecha_hora":
            if value < datetime.datetime.now(timezone.utc):
                raise ValueError(
                    "La fecha y hora de la cita no pueden ser en el pasado"
                )
            cita_existente = (
                db.query(Cita)
                .filter(Cita.fecha_hora == value, Cita.id_medico == cita.id_medico)
                .first()
            )
            if cita_existente and cita_existente.id_cita != id_cita:
                raise ValueError("Ya existe una cita programada para esa fecha y hora")

        setattr(cita, key, value)

    cita.id_usuario_edicion = id_usuario_edicion

    db.commit()
    db.refresh(cita)

    return cita


def eliminar_cita(id_cita: UUID) -> bool:
    """
    Elimina una cita por su identificador.
    """

    cita = obtener_por_id(id_cita)

    if cita:
        db.delete(cita)
        db.commit()
        return True

    return False
