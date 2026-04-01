from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from src.endpoints.deps import DbSession
from src.crud import crud_servicio

router = APIRouter(prefix="/servicios", tags=["servicios"])


class ServicioBase(BaseModel):
    nombre: str
    costo_base: float
    descripcion: Optional[str] = None
    duracion_aproximada: Optional[str] = None


class ServicioCreate(ServicioBase):
    id_usuario: UUID


class ServicioRead(ServicioBase):
    id_servicio: UUID

    class Config:
        from_attributes = True


@router.post("", response_model=ServicioRead, status_code=status.HTTP_201_CREATED)
def crear_servicio(body: ServicioCreate, db: DbSession):
    try:
        return crud_servicio.crear_servicio(
            db=db,
            nombre=body.nombre,
            costo_base=body.costo_base,
            id_usuario=body.id_usuario,
            descripcion=body.descripcion,
            duracion_aproximada=body.duracion_aproximada,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[ServicioRead])
def listar_servicios(db: DbSession):
    return crud_servicio.obtener_todos(db=db)
