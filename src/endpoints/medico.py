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


class MedicoRead(MedicoBase):
    id_medico: UUID
    id_usuario: UUID

    class Config:
        from_attributes = True


@router.post("", response_model=MedicoRead, status_code=status.HTTP_201_CREATED)
def crear_medico(body: MedicoCreate, db: DbSession):
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
    return crud_medico.obtener_todos_medicos(db=db)
