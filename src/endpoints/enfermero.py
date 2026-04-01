from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db

from src.crud import crud_enfermero

router = APIRouter(prefix="/enfermeros", tags=["enfermeros"])


class EnfermeroCreate(BaseModel):
    id_usuario: UUID
    nombre: str
    telefono: str
    area: str
    turno: str


class EnfermeroUpdate(BaseModel):
    id_usuario: Optional[UUID] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    area: Optional[str] = None
    turno: Optional[str] = None


class EnfermeroRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_enfermero: UUID
    id_usuario: UUID
    nombre: str
    telefono: str
    area: str
    turno: str


@router.get("", response_model=List[EnfermeroRead])
def listar_enfermeros(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[EnfermeroRead]:
    return crud_enfermero.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_enfermero}", response_model=EnfermeroRead)
def obtener_enfermero(
    id_enfermero: UUID, db: Session = Depends(get_db)
) -> EnfermeroRead:
    e = crud_enfermero.obtener_por_id(db, id_enfermero)
    if not e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
        )
    return e


@router.post("", response_model=EnfermeroRead, status_code=status.HTTP_201_CREATED)
def crear_enfermero(
    body: EnfermeroCreate, db: Session = Depends(get_db)
) -> EnfermeroRead:
    e = crud_enfermero.crear_enfermero(
        db,
        id_usuario=body.id_usuario,
        nombre=body.nombre,
        telefono=body.telefono,
        area=body.area,
        turno=body.turno,
    )
    return e


@router.put("/{id_enfermero}", response_model=EnfermeroRead)
def actualizar_enfermero(
    id_enfermero: UUID, body: EnfermeroUpdate, db: Session = Depends(get_db)
) -> EnfermeroRead:

    data = body.model_dump(exclude_unset=True)
    e = crud_enfermero.actualizar_enfermero(db, id_enfermero, **data)
    if not e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
        )
    return e


@router.delete("/{id_enfermero}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_enfermero(id_enfermero: UUID, db: Session = Depends(get_db)) -> None:
    if not crud_enfermero.eliminar_enfermero(db, id_enfermero):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Enfermero no encontrado"
        )
