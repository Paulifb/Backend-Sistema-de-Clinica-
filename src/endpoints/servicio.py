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


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    costo_base: Optional[float] = None
    descripcion: Optional[str] = None
    duracion_aproximada: Optional[str] = None
    id_usuario: UUID


class ServicioRead(ServicioBase):
    id_servicio: UUID
    id_usuario: UUID

    class Config:
        from_attributes = True


@router.post("", response_model=ServicioRead, status_code=status.HTTP_201_CREATED)
def crear_servicio(body: ServicioCreate, db: DbSession):
    """
    Registra un nuevo servicio en el catálogo de la clínica.

    Valida que el costo base sea un valor positivo y que el usuario exista.
    """
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
    """
    Obtiene la lista completa de servicios disponibles.
    """
    return crud_servicio.obtener_todos_servicios(db=db)


@router.get("/{id_servicio}", response_model=ServicioRead)
def obtener_servicio(id_servicio: UUID, db: DbSession):
    """
    Consulta la información detallada de un servicio específico.
    """
    servicio = crud_servicio.obtener_servicio_por_id(db=db, id_servicio=id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.put("/{id_servicio}", response_model=ServicioRead)
def actualizar_servicio(id_servicio: UUID, body: ServicioUpdate, db: DbSession):
    """
    Actualiza los datos de un servicio existente de forma parcial.

    Requiere el ID del usuario responsable para el registro de la modificación.
    """
    try:
        update_data = body.model_dump(exclude_unset=True)
        id_usuario = update_data.pop("id_usuario")

        servicio = crud_servicio.actualizar_servicio(
            db=db, id_servicio=id_servicio, id_usuario=id_usuario, **update_data
        )
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return servicio
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(id_servicio: UUID, db: DbSession):
    """
    Elimina un servicio del sistema mediante su identificador.
    """
    exito = crud_servicio.eliminar_servicio(db=db, id_servicio=id_servicio)
    if not exito:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return None
