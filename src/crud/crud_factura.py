"""CRUD para Factura"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from src.database.config import SessionLocal
from src.entities.factura import Factura
from src.entities.cita import Cita

db = SessionLocal()


def crear_factura(
    id_cita: UUID,
    total: float,
    estado_pago: str,
    fecha_pago: datetime,
    id_usuario_creacion: UUID,
    metodo_pago: Optional[str] = None,
) -> Factura:

    if total <= 0:
        raise ValueError("El total debe ser mayor a 0")

    if fecha_pago > datetime.now(timezone.utc):
        raise ValueError("La fecha de pago no puede ser futura")

    if not db.query(Cita).filter(Cita.id_cita == id_cita).first():
        raise ValueError("La cita no existe")

    estado_pago = estado_pago.strip().capitalize()

    estados_validos = ["Pendiente", "Pagado", "Cancelado"]
    if estado_pago not in estados_validos:
        raise ValueError("Estado de pago inválido")

    factura_existente = db.query(Factura).filter(Factura.id_cita == id_cita).first()

    if factura_existente:
        raise ValueError("Ya existe una factura para esta cita")

    if metodo_pago:
        metodo_pago = metodo_pago.strip().capitalize()
        metodos_validos = ["Efectivo", "Tarjeta", "Transferencia"]
        if metodo_pago not in metodos_validos:
            raise ValueError("Método de pago inválido")

    factura = Factura(
        id_cita=id_cita,
        total=total,
        metodo_pago=metodo_pago,
        estado_pago=estado_pago,
        fecha_pago=fecha_pago,
        id_usuario_creacion=id_usuario_creacion,
    )

    db.add(factura)
    db.commit()
    db.refresh(factura)

    return factura


def obtener_por_id(id_factura: UUID) -> Optional[Factura]:
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def obtener_todos() -> List[Factura]:
    return db.query(Factura).all()


def actualizar(id_factura: UUID, id_usuario_edita: UUID, **kwargs) -> Optional[Factura]:

    factura = obtener_por_id(id_factura)

    if not factura:
        return None

    estados_validos = ["Pendiente", "Pagado", "Cancelado"]

    for key, value in kwargs.items():

        if isinstance(value, str):
            value = value.strip()

        if key == "estado_pago":
            value = value.capitalize()
            if value not in estados_validos:
                raise ValueError("Estado de pago inválido")

        if key == "total":
            if value <= 0:
                raise ValueError("El total debe ser mayor a 0")

        if key == "fecha_pago":
            if value > datetime.now():
                raise ValueError("La fecha de pago no puede ser futura")

        setattr(factura, key, value)

    factura.id_usuario_edita = id_usuario_edita

    db.commit()
    db.refresh(factura)

    return factura


def eliminar(id_factura: UUID) -> bool:

    factura = obtener_por_id(id_factura)

    if not factura:
        return False

    db.delete(factura)
    db.commit()

    return True
