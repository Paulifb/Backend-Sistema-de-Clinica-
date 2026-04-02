"""
Endpoints de la entidad Paciente.

Este módulo define las rutas (endpoints) para gestionar los pacientes del sistema,
incluyendo operaciones de creación, consulta, actualización y eliminación.

Cada endpoint se comunica con la capa CRUD para ejecutar la lógica de negocio
y maneja posibles errores devolviendo respuestas HTTP adecuadas.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import paciente as crud_paciente

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


class PacienteCreate(BaseModel):
    nombre: str
    fecha_nacimiento: datetime
    genero: str
    tipo_afiliacion: str
    id_eps: UUID
    id_usuario: UUID
    id_usuario_creacion: UUID
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = None
    tipo_afiliacion: Optional[str] = None
    id_eps: Optional[UUID] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_usuario_edicion: UUID


class PacienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_paciente: UUID
    nombre: str
    fecha_nacimiento: datetime
    genero: str
    tipo_afiliacion: str

    telefono: Optional[str]
    direccion: Optional[str]

    id_eps: UUID
    id_usuario: UUID

    fecha_creacion: Optional[datetime]
    fecha_edicion: Optional[datetime]

    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID]


@router.get("", response_model=List[PacienteRead])
def listar_pacientes(db: DbSession):

    return crud_paciente.obtener_todos()


@router.get("/{id_paciente}", response_model=PacienteRead)
def obtener_paciente(db: DbSession, id_paciente: UUID):

    paciente = crud_paciente.obtener_por_id(id_paciente)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@router.post("", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def crear_paciente(db: DbSession, body: PacienteCreate):

    try:
        return crud_paciente.crear_paciente(
            nombre=body.nombre,
            fecha_nacimiento=body.fecha_nacimiento,
            genero=body.genero,
            tipo_afiliacion=body.tipo_afiliacion,
            id_eps=body.id_eps,
            id_usuario=body.id_usuario,
            id_usuario_creacion=body.id_usuario_creacion,
            telefono=body.telefono,
            direccion=body.direccion,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))


@router.put("/{id_paciente}", response_model=PacienteRead)
def actualizar_paciente(db: DbSession, id_paciente: UUID, body: PacienteUpdate):

    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})

    try:
        paciente = crud_paciente.actualizar(
            id_paciente=id_paciente,
            id_usuario_edicion=body.id_usuario_edicion,
            **data,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    if not paciente:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Paciente no encontrado")

    return paciente


@router.delete("/{id_paciente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(db: DbSession, id_paciente: UUID):

    if not crud_paciente.eliminar(id_paciente):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Paciente no encontrado")
