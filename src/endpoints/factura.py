"""
Endpoints de la entidad Factura.

Este módulo define las rutas (endpoints) para gestionar las facturas
del sistema, incluyendo operaciones de creación, consulta, actualización
y eliminación.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import crud_factura


router = APIRouter(prefix="/facturas", tags=["Facturas"])


class FacturaCreate(BaseModel):
    """
    Modelo de datos para crear una factura.

    Contiene la información necesaria para registrar un nuevo comprobante de pago.
    """

    id_cita: UUID
    total: float
    metodo_pago: Optional[str] = None
    estado_pago: str
    fecha_pago: datetime
    id_usuario_creacion: UUID


class FacturaUpdate(BaseModel):
    """
    Modelo de datos para actualizar una factura.

    Permite modificar valores existentes y registrar el usuario que edita.
    """

    total: Optional[float] = None
    metodo_pago: Optional[str] = None
    estado_pago: Optional[str] = None
    fecha_pago: Optional[datetime] = None
    id_usuario_edicion: UUID


class FacturaRead(BaseModel):
    """
    Modelo de lectura para mostrar una factura.

    Representa cómo se devuelve una factura al cliente.
    """

    model_config = ConfigDict(from_attributes=True)

    id_factura: UUID
    id_cita: UUID
    total: float
    metodo_pago: Optional[str]
    estado_pago: str
    fecha_pago: datetime

    fecha_creacion: Optional[datetime]
    fecha_edicion: Optional[datetime]

    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID]


@router.get("", response_model=List[FacturaRead])
def listar_facturas(db: DbSession, skip: int = 0, limit: int = 100):
    """
    Lista todas las facturas registradas.

    Permite paginar los resultados usando skip y limit.
    """
    return crud_factura.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(db: DbSession, id_factura: UUID):
    """
    Obtiene una factura por su ID.

    Retorna la factura si existe; de lo contrario devuelve error 404.
    """
    f = crud_factura.obtener_por_id(db, id_factura)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.post("", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(db: DbSession, body: FacturaCreate):
    """
    Crea una nueva factura.

    Valida que los datos sean correctos antes de registrarla.
    """
    try:
        return crud_factura.crear_factura(
            db,
            id_cita=body.id_cita,
            total=body.total,
            metodo_pago=body.metodo_pago,
            estado_pago=body.estado_pago,
            fecha_pago=body.fecha_pago,
            id_usuario_creacion=body.id_usuario_creacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_factura}", response_model=FacturaRead)
def actualizar_factura(db: DbSession, id_factura: UUID, body: FacturaUpdate):
    """
    Actualiza una factura existente.

    Solo modifica los campos enviados y registra el usuario que la edita.
    """
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})

    try:
        f = crud_factura.actualizar(
            db,
            id_factura,
            id_usuario_edicion=body.id_usuario_edicion,
            **data,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.delete("/{id_factura}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(db: DbSession, id_factura: UUID):
    """
    Elimina una factura por su ID.

    Devuelve error 404 si la factura no existe.
    """
    if not crud_factura.eliminar(db, id_factura):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
