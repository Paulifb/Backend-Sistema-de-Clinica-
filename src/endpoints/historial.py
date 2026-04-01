"""
Endpoints para la gestión de historiales clínicos.

Este módulo define las rutas de la API para realizar operaciones CRUD
sobre la entidad Historial. Incluye la creación, consulta, actualización
y eliminación de historiales, así como la trazabilidad mediante usuarios
de creación y edición.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.crud import crud_historial

router = APIRouter(prefix="/historiales", tags=["historiales"])


class HistorialCreate(BaseModel):
    """
    Modelo de datos para la creación de un historial clínico.

    Contiene la información necesaria para registrar un nuevo historial,
    incluyendo la relación con la cita, el enfermero y el usuario creador.
    """

    id_cita: UUID
    id_enfermero: UUID
    diagnostico: str
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_creacion: UUID


class HistorialUpdate(BaseModel):
    """
    Modelo de datos para la actualización de un historial clínico.

    Permite modificar únicamente los campos clínicos del historial.
    El usuario que realiza la edición es obligatorio para mantener
    la trazabilidad del registro.
    """

    diagnostico: Optional[str] = None
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_edicion: UUID


class HistorialRead(BaseModel):
    """
    Modelo de respuesta para un historial clínico.

    Representa la información que se devuelve al cliente,
    incluyendo datos de trazabilidad como fechas y usuarios.
    """

    model_config = ConfigDict(from_attributes=True)

    id_historial: UUID
    id_cita: UUID
    id_enfermero: UUID
    diagnostico: str
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[HistorialRead])
def listar_historiales(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[HistorialRead]:
    """
    Obtiene la lista de historiales clínicos.

    Permite paginar los resultados mediante los parámetros skip y limit.

    Returns:
        Lista de historiales clínicos.
    """
    return crud_historial.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_historial}", response_model=HistorialRead)
def obtener_historial(
    id_historial: UUID, db: Session = Depends(get_db)
) -> HistorialRead:
    """
    Obtiene un historial clínico por su identificador.

    Raises:
        HTTPException: Si el historial no existe.

    Returns:
        Historial clínico encontrado.
    """
    h = crud_historial.obtener_por_id(db, id_historial)

    if not h:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
        )
    return h


@router.post("", response_model=HistorialRead, status_code=status.HTTP_201_CREATED)
def crear_historial(
    body: HistorialCreate, db: Session = Depends(get_db)
) -> HistorialRead:
    """
    Crea un nuevo historial clínico.

    Valida la información a través del CRUD y captura errores de negocio.

    Raises:
        HTTPException: Si ocurre un error de validación.

    Returns:
        Historial clínico creado.
    """
    try:
        return crud_historial.crear_historial(
            db,
            id_cita=body.id_cita,
            id_enfermero=body.id_enfermero,
            diagnostico=body.diagnostico,
            observaciones_medicas=body.observaciones_medicas,
            indicaciones_enfermeria=body.indicaciones_enfermeria,
            observaciones_enfermeria=body.observaciones_enfermeria,
            id_usuario_creacion=body.id_usuario_creacion,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_historial}", response_model=HistorialRead)
def actualizar_historial(
    id_historial: UUID, body: HistorialUpdate, db: Session = Depends(get_db)
) -> HistorialRead:
    """
    Actualiza un historial clínico existente.

    Solo permite modificar los campos clínicos. Se requiere el usuario
    que realiza la edición para mantener la trazabilidad.

    Raises:
        HTTPException: Si el historial no existe o hay errores de validación.

    Returns:
        Historial clínico actualizado.
    """
    try:
        data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})

        h = crud_historial.actualizar_historial(
            db, id_historial, id_usuario_edicion=body.id_usuario_edicion, **data
        )

        if not h:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
            )
        return h

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_historial}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_historial(id_historial: UUID, db: Session = Depends(get_db)) -> None:
    """
    Elimina un historial clínico por su identificador.

    Raises:
        HTTPException: Si el historial no existe.
    """
    if not crud_historial.eliminar_historial(db, id_historial):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
        )
