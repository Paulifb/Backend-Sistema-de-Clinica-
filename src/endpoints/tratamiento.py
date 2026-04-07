"""
Endpoints de la entidad Tratamiento.

Este módulo define las rutas (endpoints) para gestionar los tratamientos
registrados en el historial clínico de los pacientes.
Incluye operaciones para crear, consultar, actualizar y eliminar tratamientos.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import crud_tratamiento

router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


class TratamientoCreate(BaseModel):
    """
    Modelo de datos para crear un tratamiento.

    Contiene los datos necesarios para registrar un nuevo tratamiento en un historial clínico.
    """

    id_historial: UUID
    nombre_tratamiento: str
    descripcion: Optional[str] = None
    dosis: str
    duracion: int


class TratamientoUpdate(BaseModel):
    """
    Modelo de datos para actualizar un tratamiento.

    Permite modificar uno o varios campos del tratamiento.
    """

    id_historial: Optional[UUID] = None
    nombre_tratamiento: Optional[str] = None
    descripcion: Optional[str] = None
    dosis: Optional[str] = None
    duracion: Optional[int] = None


class TratamientoRead(BaseModel):
    """
    Modelo de lectura para mostrar un tratamiento.

    Representa cómo se devuelve un tratamiento al cliente.
    """

    model_config = ConfigDict(from_attributes=True)

    id_tratamiento: UUID
    id_historial: UUID
    nombre_tratamiento: str
    descripcion: Optional[str]
    dosis: str
    duracion: int


@router.get("", response_model=List[TratamientoRead])
def listar_tratamientos(db: DbSession):
    """
    Lista todos los tratamientos registrados.

    Devuelve una colección con los tratamientos existentes.
    """
    return crud_tratamiento.obtener_todos(db)


@router.get("/{id_tratamiento}", response_model=TratamientoRead)
def obtener_tratamiento(db: DbSession, id_tratamiento: UUID):
    """
    Obtiene un tratamiento por su ID.

    Retorna el tratamiento si existe; de lo contrario lanza un error 404.
    """
    tratamiento = crud_tratamiento.obtener_por_id(db, id_tratamiento)
    if not tratamiento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")
    return tratamiento


@router.post("", response_model=TratamientoRead, status_code=status.HTTP_201_CREATED)
def crear_tratamiento(db: DbSession, body: TratamientoCreate):
    """
    Crea un nuevo tratamiento.

    Valida y registra la información dentro del historial correspondiente.
    """
    try:
        return crud_tratamiento.crear(
            db,
            id_historial=body.id_historial,
            nombre_tratamiento=body.nombre_tratamiento,
            descripcion=body.descripcion,
            dosis=body.dosis,
            duracion=body.duracion,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.put("/{id_tratamiento}", response_model=TratamientoRead)
def actualizar_tratamiento(
    db: DbSession, id_tratamiento: UUID, body: TratamientoUpdate
):
    """
    Actualiza un tratamiento existente.

    Solo modifica los campos enviados en la solicitud.
    """
    data = body.model_dump(exclude_unset=True)

    try:
        tratamiento = crud_tratamiento.actualizar(db, id_tratamiento, **data)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    if not tratamiento:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")

    return tratamiento


@router.delete("/{id_tratamiento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tratamiento(db: DbSession, id_tratamiento: UUID):
    """
    Elimina un tratamiento por su ID.

    Retorna error 404 si el tratamiento no existe.
    """
    if not crud_tratamiento.eliminar(db, id_tratamiento):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tratamiento no encontrado")
