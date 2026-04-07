"""
Endpoints de la entidad Paciente.

Este módulo define las rutas (endpoints) para gestionar los pacientes del sistema,
incluyendo operaciones de creación, consulta, actualización y eliminación.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import crud_paciente

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


class PacienteCreate(BaseModel):
    """
    Modelo de datos para crear un paciente.

    Incluye los datos básicos y la información de afiliación del paciente.
    """

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
    """
    Modelo de datos para actualizar un paciente.

    Permite modificar campos específicos y registra el usuario que edita.
    """

    nombre: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = None
    tipo_afiliacion: Optional[str] = None
    id_eps: Optional[UUID] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    id_usuario_edicion: UUID


class PacienteRead(BaseModel):
    """
    Modelo de lectura para mostrar un paciente.

    Representa cómo se devuelve la información completa de un paciente.
    """

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
    """
    Lista todos los pacientes registrados.

    Retorna una colección con la información básica de cada paciente.
    """
    return crud_paciente.obtener_todos(db)


@router.get("/{id_paciente}", response_model=PacienteRead)
def obtener_paciente(db: DbSession, id_paciente: UUID):
    """
    Obtiene un paciente por su ID.

    Retorna el paciente si existe; si no, genera un error 404.
    """
    paciente = crud_paciente.obtener_por_id(db, id_paciente)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente


@router.post("", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def crear_paciente(db: DbSession, body: PacienteCreate):
    """
    Crea un nuevo paciente.

    Valida la información y registra el paciente en el sistema.
    """
    try:
        return crud_paciente.crear_paciente(
            db=db,
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_paciente}", response_model=PacienteRead)
def actualizar_paciente(db: DbSession, id_paciente: UUID, body: PacienteUpdate):
    """
    Actualiza los datos de un paciente existente.

    Solo se modifican los campos enviados, registrando el usuario editor.
    """
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})

    try:
        paciente = crud_paciente.actualizar(
            db=db,
            id_paciente=id_paciente,
            id_usuario_edicion=body.id_usuario_edicion,
            **data,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
        )

    return paciente


@router.delete("/{id_paciente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(db: DbSession, id_paciente: UUID):
    """
    Elimina un paciente del sistema.

    Retorna error 404 si el paciente no existe.
    """
    if not crud_paciente.eliminar(db, id_paciente):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente no encontrado"
        )
