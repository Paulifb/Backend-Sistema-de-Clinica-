"""
Endpoints de la entidad EPS.

Este módulo define las rutas (endpoints) para gestionar las entidades de EPS
dentro del sistema de clínica. Incluye operaciones para crear, consultar,
actualizar y eliminar registros de EPS.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import crud_eps


router = APIRouter(prefix="/eps", tags=["EPS"])


class EPSCreate(BaseModel):
    """
    Modelo de datos para crear una EPS.

    Contiene los campos necesarios para registrar un nuevo proveedor de salud.
    """

    nombre: str
    correo: Optional[str] = None
    telefono: str
    direccion: str
    ciudad: Optional[str] = None


class EPSUpdate(BaseModel):
    """
    Modelo de datos para actualizar una EPS.

    Permite modificar uno o varios campos de un registro existente.
    """

    nombre: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None


class EPSRead(BaseModel):
    """
    Modelo de datos para la lectura de una EPS.

    Representa cómo se devuelve un registro de EPS al cliente.
    """

    model_config = ConfigDict(from_attributes=True)

    id_eps: UUID
    nombre: str
    correo: Optional[str]
    telefono: str
    direccion: str
    ciudad: Optional[str]


@router.get("", response_model=List[EPSRead])
def listar_eps(db: DbSession, skip: int = 0, limit: int = 100):
    """
    Lista todas las EPS registradas.

    Permite paginar los resultados mediante skip y limit.
    """
    return crud_eps.listar(db, skip=skip, limit=limit)


@router.get("/{id_eps}", response_model=EPSRead)
def obtener_eps(db: DbSession, id_eps: UUID):
    """
    Obtiene una EPS por su ID.

    Retorna el registro si existe, de lo contrario genera un error 404.
    """
    eps = crud_eps.obtener(db, id_eps)
    if not eps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
    return eps


@router.post("", response_model=EPSRead, status_code=status.HTTP_201_CREATED)
def crear_eps(db: DbSession, body: EPSCreate):
    """
    Crea una nueva EPS.

    Valida que no exista otra EPS con el mismo nombre.
    """
    try:
        return crud_eps.crear(
            db,
            nombre=body.nombre,
            correo=body.correo,
            telefono=body.telefono,
            direccion=body.direccion,
            ciudad=body.ciudad,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_eps}", response_model=EPSRead)
def actualizar_eps(db: DbSession, id_eps: UUID, body: EPSUpdate):
    """
    Actualiza una EPS existente.

    Solo modifica los campos enviados en la petición.
    """
    data = body.model_dump(exclude_unset=True)

    try:
        eps = crud_eps.actualizar(db, id_eps, **data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not eps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
    return eps


@router.delete("/{id_eps}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_eps(db: DbSession, id_eps: UUID):
    """
    Elimina una EPS por su ID.

    Si no existe, responde con un error 404.
    """
    if not crud_eps.eliminar(db, id_eps):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EPS no encontrada"
        )
