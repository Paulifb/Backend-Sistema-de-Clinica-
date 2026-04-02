"""
Endpoints para la gestión de enfermeros.

Este módulo define las rutas de la API para realizar operaciones CRUD
sobre la entidad Enfermero. Permite crear, consultar, actualizar y eliminar
registros, aplicando validaciones a través del módulo CRUD.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from .deps import DbSession
from src.crud import crud_enfermero

router = APIRouter(prefix="/enfermeros", tags=["enfermeros"])


class EnfermeroCreate(BaseModel):
    """
    Modelo de datos para la creación de un enfermero.

    Contiene la información básica requerida para registrar
    un nuevo enfermero en el sistema.
    """

    id_usuario: UUID
    nombre: str = Field(..., min_length=1, max_length=120)
    telefono: str = Field(..., min_length=7, max_length=20)
    area: str
    turno: str


class EnfermeroUpdate(BaseModel):
    """
    Modelo de datos para la actualización de un enfermero.

    Permite modificar uno o varios campos del registro.
    Todos los campos son opcionales.
    """

    id_usuario: Optional[UUID] = None
    nombre: Optional[str] = Field(None, min_length=1, max_length=120)
    telefono: Optional[str] = Field(None, min_length=7, max_length=20)
    area: Optional[str] = None
    turno: Optional[str] = None


class EnfermeroRead(BaseModel):
    """
    Modelo de respuesta para un enfermero.

    Representa la información que se devuelve al cliente.
    """

    model_config = ConfigDict(from_attributes=True)

    id_enfermero: UUID
    id_usuario: UUID
    nombre: str
    telefono: str
    area: str
    turno: str


@router.get("", response_model=List[EnfermeroRead])
def listar_enfermeros(
    db: DbSession, skip: int = 0, limit: int = 100
) -> List[EnfermeroRead]:
    """
    Obtiene la lista de enfermeros.

    Permite paginar los resultados mediante skip y limit.

    Returns:
        Lista de enfermeros.
    """
    return crud_enfermero.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_enfermero}", response_model=EnfermeroRead)
def obtener_enfermero(id_enfermero: UUID, db: DbSession) -> EnfermeroRead:
    """
    Obtiene un enfermero por su identificador.

    Raises:
        HTTPException: Si el enfermero no existe.

    Returns:
        Enfermero encontrado.
    """
    e = crud_enfermero.obtener_por_id(db, id_enfermero)

    if not e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
        )
    return e


@router.post("", response_model=EnfermeroRead, status_code=status.HTTP_201_CREATED)
def crear_enfermero(body: EnfermeroCreate, db: DbSession) -> EnfermeroRead:
    """
    Crea un nuevo enfermero.

    Valida la información mediante el CRUD.

    Raises:
        HTTPException: Si hay errores de validación.

    Returns:
        Enfermero creado.
    """
    try:
        return crud_enfermero.crear_enfermero(
            db,
            id_usuario=body.id_usuario,
            nombre=body.nombre,
            telefono=body.telefono,
            area=body.area,
            turno=body.turno,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_enfermero}", response_model=EnfermeroRead)
def actualizar_enfermero(
    id_enfermero: UUID, body: EnfermeroUpdate, db: DbSession
) -> EnfermeroRead:
    """
    Actualiza un enfermero existente.

    Permite modificar solo los campos enviados en la solicitud.

    Raises:
        HTTPException: Si el enfermero no existe o hay errores de validación.

    Returns:
        Enfermero actualizado.
    """

    data = body.model_dump(exclude_unset=True)

    try:
        e = crud_enfermero.actualizar_enfermero(db, id_enfermero, **data)

        if not e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
            )
        return e

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_enfermero}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_enfermero(id_enfermero: UUID, db: DbSession) -> None:
    """
    Elimina un enfermero por su identificador.

    Raises:
        HTTPException: Si el enfermero no existe.
    """
    if not crud_enfermero.eliminar_enfermero(db, id_enfermero):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
        )
