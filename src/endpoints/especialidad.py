from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from src.endpoints.deps import DbSession
from src.crud import crud_especialidad

router = APIRouter(prefix="/especialidades", tags=["especialidades"])


class EspecialidadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class EspecialidadCreate(EspecialidadBase):
    id_usuario: UUID


class EspecialidadRead(EspecialidadBase):
    id_especialidad: UUID
    id_usuario: UUID

    class Config:
        from_attributes = True


@router.post("", response_model=EspecialidadRead, status_code=status.HTTP_201_CREATED)
def crear_especialidad(body: EspecialidadCreate, db: DbSession):
    try:
        # Ahora pasamos 'db' como primer argumento
        return crud_especialidad.crear_especialidad(
            db=db,
            nombre=body.nombre,
            id_usuario=body.id_usuario,
            descripcion=body.descripcion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[EspecialidadRead])
def listar_especialidades(db: DbSession):
    return crud_especialidad.obtener_todas(db=db)


@router.get("/{id_especialidad}", response_model=EspecialidadRead)
def obtener_especialidad(id_especialidad: UUID, db: DbSession):
    especialidad = crud_especialidad.obtener_por_id(
        db=db, id_especialidad=id_especialidad
    )
    if not especialidad:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    return especialidad
