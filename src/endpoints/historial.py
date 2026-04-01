from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db

from src.crud import crud_historial

router = APIRouter(prefix="/historiales", tags=["historiales"])


class HistorialCreate(BaseModel):
    id_cita: UUID
    id_enfermero: UUID
    diagnostico: str
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_creacion: UUID


class HistorialUpdate(BaseModel):
    id_cita: Optional[UUID] = None
    id_enfermero: Optional[UUID] = None
    diagnostico: Optional[str] = None
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_edicion: Optional[UUID] = None


class HistorialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_historial: UUID
    id_cita: UUID
    id_enfermero: UUID
    diagnostico: str
    observaciones_medicas: Optional[str] = None
    indicaciones_enfermeria: Optional[str] = None
    observaciones_enfermeria: Optional[str] = None
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[HistorialRead])
def listar_historiales(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[HistorialRead]:
    return crud_historial.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_historial}", response_model=HistorialRead)
def obtener_historial(
    id_historial: UUID, db: Session = Depends(get_db)
) -> HistorialRead:
    h = crud_historial.obtener_por_id(db, id_historial)
    if not h:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
        )
    return h


@router.post("", response_model=HistorialRead, status_code=status.HTTP_201_CREATED)
def crear_historial(
    body: HistorialCreate, db: Session = Depends(get_db)
) -> HistorialRead:
    h = crud_historial.crear_historial(
        db,
        id_cita=body.id_cita,
        id_enfermero=body.id_enfermero,
        diagnostico=body.diagnostico,
        observaciones_medicas=body.observaciones_medicas,
        indicaciones_enfermeria=body.indicaciones_enfermeria,
        observaciones_enfermeria=body.observaciones_enfermeria,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return h


@router.put("/{id_historial}", response_model=HistorialRead)
def actualizar_historial(
    id_historial: UUID, body: HistorialUpdate, db: Session = Depends(get_db)
) -> HistorialRead:
    id_edita = body.id_usuario_edicion
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})
    h = crud_historial.actualizar_historial(
        db, id_historial, id_usuario_edicion=id_edita, **data
    )
    if not h:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
        )
    return h


@router.delete("/{id_historial}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_historial(id_historial: UUID, db: Session = Depends(get_db)) -> None:
    if not crud_historial.eliminar_historial(db, id_historial):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Historial no encontrado"
        )
