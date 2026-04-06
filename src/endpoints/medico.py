from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from src.endpoints.deps import DbSession
from src.crud import crud_medico

router = APIRouter(prefix="/medicos", tags=["medicos"])


class MedicoBase(BaseModel):
    nombre: str
    id_especialidad: UUID
    telefono: Optional[str] = None


class MedicoCreate(MedicoBase):
    id_usuario: UUID


class MedicoUpdate(BaseModel):
    nombre: Optional[str] = None
    id_especialidad: Optional[UUID] = None
    telefono: Optional[str] = None
    id_usuario: UUID


class MedicoRead(MedicoBase):
    id_medico: UUID
    id_usuario: UUID

    class Config:
        from_attributes = True


@router.post("", response_model=MedicoRead, status_code=status.HTTP_201_CREATED)
def crear_medico(body: MedicoCreate, db: DbSession):
    """
    Registra un nuevo médico en el sistema.

    Verifica que tanto el usuario responsable como la especialidad asignada existan.
    """
    try:
        return crud_medico.crear_medico(
            db=db,
            nombre=body.nombre,
            id_usuario=body.id_usuario,
            id_especialidad=body.id_especialidad,
            telefono=body.telefono,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[MedicoRead])
def listar_medicos(db: DbSession):
    """
    Obtiene el listado completo de todos los médicos registrados.
    """
    return crud_medico.obtener_todos_medicos(db=db)


@router.get("/{id_medico}", response_model=MedicoRead)
def obtener_medico(id_medico: UUID, db: DbSession):
    """
    Recupera la información detallada de un médico específico por su ID.
    """
    medico = crud_medico.obtener_medico_por_id(db=db, id_medico=id_medico)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico


@router.put("/{id_medico}", response_model=MedicoRead)
def actualizar_medico(id_medico: UUID, body: MedicoUpdate, db: DbSession):
    """
    Actualiza los datos de un médico existente.

    Permite modificar nombre, teléfono o especialidad, validando la trazabilidad del usuario.
    """
    try:
        update_data = body.model_dump(exclude_unset=True)
        id_usuario = update_data.pop("id_usuario")

        medico = crud_medico.actualizar_medico(
            db=db, id_medico=id_medico, id_usuario=id_usuario, **update_data
        )
        if not medico:
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        return medico
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id_medico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medico(id_medico: UUID, db: DbSession):
    """
    Elimina el registro de un médico del sistema.
    """
    exito = crud_medico.eliminar_medico(db=db, id_medico=id_medico)
    if not exito:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return None
