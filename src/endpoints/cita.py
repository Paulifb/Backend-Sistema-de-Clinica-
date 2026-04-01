"""
Endpoints de la entidad Cita.

Este módulo define las rutas (endpoints) para gestionar las citas médicas
del sistema, incluyendo operaciones de creación, consulta, actualización
y eliminación.

Cada endpoint se comunica con la capa CRUD para ejecutar la lógica de negocio
y maneja posibles errores devolviendo respuestas HTTP adecuadas.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.crud import crud_cita

router = APIRouter(prefix="/citas", tags=["citas"])


class CitaCreate(BaseModel):
    """
    Modelo de datos para la creación de una cita.

    Atributos:
        id_paciente: Identificador del paciente.
        id_medico: Identificador del médico.
        id_servicio: Identificador del servicio.
        fecha_hora: Fecha y hora programada para la cita.
        motivo: Motivo de la consulta.
        estado: Estado inicial de la cita (por defecto "pendiente").
        id_usuario_creacion: Usuario que crea la cita.
    """

    id_paciente: UUID
    id_medico: UUID
    id_servicio: UUID
    fecha_hora: datetime
    motivo: str
    estado: str = "pendiente"
    id_usuario_creacion: UUID


class CitaUpdate(BaseModel):
    """
    Modelo de datos para la actualización de una cita.

    Todos los campos son opcionales excepto el usuario que realiza la edición.

    Atributos:
        id_paciente: Nuevo paciente asociado (opcional).
        id_medico: Nuevo médico asociado (opcional).
        id_servicio: Nuevo servicio asociado (opcional).
        fecha_hora: Nueva fecha y hora (opcional).
        motivo: Nuevo motivo de la consulta (opcional).
        estado: Nuevo estado de la cita (opcional).
        id_usuario_edicion: Usuario que realiza la actualización.
    """

    id_paciente: Optional[UUID] = None
    id_medico: Optional[UUID] = None
    id_servicio: Optional[UUID] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class CitaRead(BaseModel):
    """
    Modelo de respuesta para la lectura de citas.

    Representa cómo se devuelven los datos al cliente.

    Atributos:
        id_cita: Identificador de la cita.
        id_paciente: Identificador del paciente.
        id_medico: Identificador del médico.
        id_servicio: Identificador del servicio.
        fecha_hora: Fecha y hora de la cita.
        motivo: Motivo de la consulta.
        estado: Estado actual de la cita.
        id_usuario_creacion: Usuario que creó la cita.
        id_usuario_edicion: Usuario que la editó (opcional).
        fecha_creacion: Fecha de creación (opcional).
        fecha_edicion: Fecha de última modificación (opcional).
    """

    model_config = ConfigDict(from_attributes=True)

    id_cita: UUID
    id_paciente: UUID
    id_medico: UUID
    id_servicio: UUID
    fecha_hora: datetime
    motivo: str
    estado: Optional[str] = None
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[CitaRead])
def listar_citas(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[CitaRead]:
    """
    Lista todas las citas registradas en el sistema.

    Args:
        db: Sesión de base de datos.
        skip: Número de registros a omitir (paginación).
        limit: Número máximo de registros a devolver.

    Returns:
        Lista de citas.
    """
    return crud_cita.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_cita}", response_model=CitaRead)
def obtener_cita(id_cita: UUID, db: Session = Depends(get_db)) -> CitaRead:
    """
    Obtiene una cita específica por su ID.

    Args:
        id_cita: Identificador de la cita.
        db: Sesión de base de datos.

    Returns:
        La cita encontrada.

    Raises:
        HTTPException 404: Si la cita no existe.
    """
    c = crud_cita.obtener_por_id(db, id_cita)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(body: CitaCreate, db: Session = Depends(get_db)) -> CitaRead:
    """
    Crea una nueva cita en el sistema.

    Args:
        body: Datos de la cita a crear.
        db: Sesión de base de datos.

    Returns:
        La cita creada.

    Raises:
        HTTPException 400: Si ocurre un error de validación.
    """
    try:
        c = crud_cita.crear_cita(
            db,
            id_paciente=body.id_paciente,
            id_medico=body.id_medico,
            id_servicio=body.id_servicio,
            fecha_hora=body.fecha_hora,
            motivo=body.motivo,
            estado=body.estado,
            id_usuario_creacion=body.id_usuario_creacion,
        )
        return c

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_cita}", response_model=CitaRead)
def actualizar_cita(
    id_cita: UUID, body: CitaUpdate, db: Session = Depends(get_db)
) -> CitaRead:
    """
    Actualiza una cita existente.

    Args:
        id_cita: Identificador de la cita.
        body: Datos a actualizar.
        db: Sesión de base de datos.

    Returns:
        La cita actualizada.

    Raises:
        HTTPException 400: Si faltan datos o hay errores de validación.
        HTTPException 404: Si la cita no existe.
    """
    try:
        id_edita = body.id_usuario_edicion
        if not id_edita:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="id_usuario_edicion es requerido para actualizar",
            )

        data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})

        c = crud_cita.actualizar_cita(db, id_cita, id_usuario_edicion=id_edita, **data)

        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
            )

        return c

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: UUID, db: Session = Depends(get_db)) -> None:
    """
    Elimina una cita del sistema.

    Args:
        id_cita: Identificador de la cita.
        db: Sesión de base de datos.

    Raises:
        HTTPException 404: Si la cita no existe.
    """
    if not crud_cita.eliminar_cita(db, id_cita):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
