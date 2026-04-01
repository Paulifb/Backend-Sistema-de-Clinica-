from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db

from src.crud import crud_cita

router = APIRouter(prefix="/citas", tags=["citas"])


class CitaCreate(BaseModel):
    id_paciente: UUID
    id_medico: UUID
    id_servicio: UUID
    fecha_hora: datetime
    motivo: str
    estado: str = "pendiente"
    id_usuario_creacion: UUID


class CitaUpdate(BaseModel):
    id_paciente: Optional[UUID] = None
    id_medico: Optional[UUID] = None
    id_servicio: Optional[UUID] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class CitaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cita: UUID
    id_paciente: UUID
    id_medico: UUID
    id_servicio: UUID
    fecha_hora: datetime
    motivo: str
    estado: Optional[str] = None
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[CitaRead])
def listar_citas(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[CitaRead]:
    return crud_cita.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_cita}", response_model=CitaRead)
def obtener_cita(id_cita: UUID, db: Session = Depends(get_db)) -> CitaRead:
    c = crud_cita.obtener_por_id(db, id_cita)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(body: CitaCreate, db: Session = Depends(get_db)) -> CitaRead:
    c = crud_cita.crear_cita(
        db,
        id_paciente=body.id_paciente,
        id_medico=body.id_medico,
        id_servicio=body.id_servicio,
        fecha_hora=body.fecha_hora,
        motivo=body.motivo,
        estado=body.estado,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return c


@router.put("/{id_cita}", response_model=CitaRead)
def actualizar_cita(
    id_cita: UUID, body: CitaUpdate, db: Session = Depends(get_db)
) -> CitaRead:
    id_edita = body.id_usuario_edicion
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})
    c = crud_cita.actualizar_cita(db, id_cita, id_usuario_edicion=id_edita, **data)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: UUID, db: Session = Depends(get_db)) -> None:
    if not crud_cita.eliminar_cita(db, id_cita):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
