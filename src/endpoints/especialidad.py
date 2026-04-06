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

class EspecialidadUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario: UUID

class EspecialidadRead(EspecialidadBase):
    id_especialidad: UUID
    id_usuario: UUID

    class Config:
        from_attributes = True

@router.post("", response_model=EspecialidadRead, status_code=status.HTTP_201_CREATED)
def crear_especialidad(body: EspecialidadCreate, db: DbSession):
    """
    Crea una nueva especialidad médica en el sistema.
    
    Valida la existencia del usuario responsable antes de la inserción.
    """
    try:
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
    """
    Recupera el listado completo de especialidades registradas en la base de datos.
    """
    return crud_especialidad.obtener_todas_especialidades(db=db)

@router.get("/{id_especialidad}", response_model=EspecialidadRead)
def obtener_especialidad(id_especialidad: UUID, db: DbSession):
    """
    Busca y devuelve una especialidad específica mediante su ID único.
    """
    especialidad = crud_especialidad.obtener_especialidad_por_id(
        db=db, id_especialidad=id_especialidad
    )
    if not especialidad:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    return especialidad

@router.put("/{id_especialidad}", response_model=EspecialidadRead)
def actualizar_especialidad(id_especialidad: UUID, body: EspecialidadUpdate, db: DbSession):
    """
    Actualiza de forma parcial o total los datos de una especialidad.
    
    Requiere el ID del usuario que realiza la modificación para fines de trazabilidad.
    """
    try:
        update_data = body.model_dump(exclude_unset=True)
        id_usuario = update_data.pop("id_usuario")
        
        especialidad = crud_especialidad.actualizar_especialidad(
            db=db,
            id_especialidad=id_especialidad,
            id_usuario=id_usuario,
            **update_data
        )
        if not especialidad:
            raise HTTPException(status_code=404, detail="Especialidad no encontrada")
        return especialidad
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_especialidad}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_especialidad(id_especialidad: UUID, db: DbSession):
    """
    Elimina permanentemente una especialidad del sistema.
    """
    exito = crud_especialidad.eliminar_especialidad(db=db, id_especialidad=id_especialidad)
    if not exito:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    return None