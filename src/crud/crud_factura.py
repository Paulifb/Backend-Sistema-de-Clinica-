"""CRUD para Factura"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.entities.factura import Factura
from src.entities.cita import Cita
from src.entities.usuario import Usuario


def crear_factura(
    db: Session,
    id_cita: UUID,
    total: float,
    estado_pago: str,
    fecha_pago: datetime,
    id_usuario_creacion: UUID,
    metodo_pago: Optional[str] = None,
) -> Factura:
    """
    Crea una nueva factura en la base de datos.

    Incluye validaciones de cita, usuario creador, estado de pago,
    método de pago y valores básicos antes de registrar la factura.
    """

    # Validaciones básicas
    if total <= 0:
        raise ValueError("El total debe ser mayor a 0")

    if fecha_pago > datetime.now(timezone.utc):
        raise ValueError("La fecha de pago no puede ser futura")

    # Validar cita existente
    if not db.query(Cita).filter(Cita.id_cita == id_cita).first():
        raise ValueError("La cita no existe")

    # Validar usuario creador
    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario_creacion).first():
        raise ValueError("El usuario especificado no existe")

    # Validar estado
    estado_pago = estado_pago.strip().capitalize()
    estados_validos = ["Pendiente", "Pagado", "Cancelado"]
    if estado_pago not in estados_validos:
        raise ValueError("Estado de pago inválido")

    # Validar que no exista una factura para esa cita
    factura_existente = db.query(Factura).filter(Factura.id_cita == id_cita).first()
    if factura_existente:
        raise ValueError("Ya existe una factura para esta cita")

    # Validar método de pago
    if metodo_pago:
        metodo_pago = metodo_pago.strip().capitalize()
        metodos_validos = ["Efectivo", "Tarjeta", "Transferencia"]
        if metodo_pago not in metodos_validos:
            raise ValueError("Método de pago inválido")

    # Crear factura
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


def obtener_por_id(db: Session, id_factura: UUID) -> Optional[Factura]:
    """
    Obtiene una factura por su ID.
    Retorna None si no existe.
    """
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def obtener_todos(db: Session) -> List[Factura]:
    """
    Obtiene y devuelve todas las facturas registradas.
    """
    return db.query(Factura).all()


def actualizar(
    db: Session,
    id_factura: UUID,
    id_usuario_edicion: UUID,
    **kwargs,
) -> Optional[Factura]:
    """
    Actualiza una factura existente.

    Verifica que la factura exista, que el usuario editor sea válido
    y aplica reglas de validación para cada campo modificado.
    """

    factura = obtener_por_id(db, id_factura)
    if not factura:
        return None

    # Validar usuario editor
    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario_edicion).first():
        raise ValueError("El usuario especificado no existe")

    # Reglas de actualización
    estados_validos = ["Pendiente", "Pagado", "Cancelado"]

    for key, value in kwargs.items():

        if isinstance(value, str):
            value = value.strip()

        if key == "estado_pago":
            value = value.capitalize()
            if value not in estados_validos:
                raise ValueError("Estado de pago inválido")

        if key == "total" and value <= 0:
            raise ValueError("El total debe ser mayor a 0")

        if key == "fecha_pago" and value > datetime.now(timezone.utc):
            raise ValueError("La fecha de pago no puede ser futura")

        setattr(factura, key, value)

    factura.id_usuario_edicion = id_usuario_edicion

    db.commit()
    db.refresh(factura)

    return factura


def eliminar(db: Session, id_factura: UUID) -> bool:
    """
    Elimina una factura por su ID.
    Retorna True si se eliminó, False si no existe.
    """
    factura = obtener_por_id(db, id_factura)
    if not factura:
        return False

    db.delete(factura)
    db.commit()

    return True
