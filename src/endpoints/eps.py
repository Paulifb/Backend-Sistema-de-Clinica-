"""
Endpoints de la entidad EPS.

Este módulo define las rutas (endpoints) para gestionar las entidades de EPS
dentro del sistema de clínica. Incluye
operaciones para crear, consultar, actualizar y eliminar registros de EPS.

Cada endpoint interactúa con la capa CRUD correspondiente para ejecutar
la lógica de negocio relacionada con la gestión de EPS, validando datos de entrada
y manejando errores mediante respuestas HTTP adecuadas.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import eps as crud_eps


router = APIRouter(prefix="/eps", tags=["EPS"])


class EPSCreate(BaseModel):

    nombre: str
    correo: Optional[str] = None
    telefono: str
    direccion: str
    ciudad: Optional[str] = None


class EPSUpdate(BaseModel):

    nombre: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None


class EPSRead(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id_eps: UUID
    nombre: str
    correo: Optional[str]
    telefono: str
    direccion: str
    ciudad: Optional[str]


@router.get("", response_model=List[EPSRead])
def listar_eps(db: DbSession, skip: int = 0, limit: int = 100):

    return crud_eps.listar(db, skip=skip, limit=limit)


@router.get("/{id_eps}", response_model=EPSRead)
def obtener_eps(db: DbSession, id_eps: UUID):

    eps = crud_eps.obtener(db, id_eps)
    if not eps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
    return eps


@router.post("", response_model=EPSRead, status_code=status.HTTP_201_CREATED)
def crear_eps(db: DbSession, body: EPSCreate):

    return crud_eps.crear(
        db,
        nombre=body.nombre,
        correo=body.correo,
        telefono=body.telefono,
        direccion=body.direccion,
        ciudad=body.ciudad,
    )


@router.put("/{id_eps}", response_model=EPSRead)
def actualizar_eps(db: DbSession, id_eps: UUID, body: EPSUpdate):

    data = body.model_dump(exclude_unset=True)
    eps = crud_eps.actualizar(db, id_eps, **data)

    if not eps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
    return eps


@router.delete("/{id_eps}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_eps(db: DbSession, id_eps: UUID):

    if not crud_eps.eliminar(db, id_eps):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
