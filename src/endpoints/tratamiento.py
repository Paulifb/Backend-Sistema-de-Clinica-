"""
Endpoints de la entidad Tratamiento.

Este módulo define las rutas (endpoints) para gestionar los tratamientos
del sistema, incluyendo operaciones de creación, consulta, actualización
y eliminación.

Cada endpoint se comunica con la capa CRUD para ejecutar la lógica de negocio
y maneja posibles errores devolviendo respuestas HTTP adecuadas.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import tratamiento as crud_tratamiento

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


class TratamientoCreate(BaseModel):
    id_historial: UUID
    nombre_tratamiento: str
    descripcion: Optional[str] = None
    dosis: str
    duracion: int


class TratamientoUpdate(BaseModel):
    id_historial: Optional[UUID] = None
    nombre_tratamiento: Optional[str] = None
    descripcion: Optional[str] = None
    dosis: Optional[str] = None
    duracion: Optional[int] = None


class TratamientoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_tratamiento: UUID
    id_historial: UUID
    nombre_tratamiento: str
    descripcion: Optional[str]
    dosis: str
    duracion: int


@router.get("", response_model=List[TratamientoRead])
def listar_tratamientos(db: DbSession):
    """Listar todos los tratamientos."""
    return crud_tratamiento.listar()


@router.get("/{id_tratamiento}", response_model=TratamientoRead)
def obtener_tratamiento(db: DbSession, id_tratamiento: UUID):

    tratamiento = crud_tratamiento.obtener(id_tratamiento)
    if not tratamiento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")
    return tratamiento


@router.post("", response_model=TratamientoRead, status_code=status.HTTP_201_CREATED)
def crear_tratamiento(db: DbSession, body: TratamientoCreate):

    return crud_tratamiento.crear(
        id_historial=body.id_historial,
        nombre_tratamiento=body.nombre_tratamiento,
        descripcion=body.descripcion,
        dosis=body.dosis,
        duracion=body.duracion,
    )


@router.put("/{id_tratamiento}", response_model=TratamientoRead)
def actualizar_tratamiento(
    db: DbSession, id_tratamiento: UUID, body: TratamientoUpdate
):

    data = body.model_dump(exclude_unset=True)
    tratamiento = crud_tratamiento.actualizar(id_tratamiento, **data)

    if not tratamiento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")

    return tratamiento


@router.delete("/{id_tratamiento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tratamiento(db: DbSession, id_tratamiento: UUID):

    if not crud_tratamiento.eliminar(id_tratamiento):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")
