import uuid
from sqlalchemy import Column, ForeignKey, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Servicio(Base):
    """
    Representa los servicios médicos o procedimientos ofrecidos por la clínica.

    Este modelo actúa como un catálogo de servicios con sus costos base
    y tiempos estimados de duración.
    """

    __tablename__ = "servicios"

    id_servicio = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Identificador único del servicio.",
    )

    nombre = Column(
        String(100),
        nullable=False,
        doc="Nombre del servicio médico (ej. Consulta General, Radiografía).",
    )

    descripcion = Column(
        Text,
        nullable=True,
        doc="Detalles adicionales sobre lo que incluye el servicio.",
    )

    costo_base = Column(
        Float,
        nullable=False,
        doc="Precio base asignado al servicio antes de impuestos o adicionales.",
    )

    duracion_aproximada = Column(
        String(50),
        nullable=True,
        doc="Tiempo estimado de duración del servicio (ej. 30 min, 1 hora).",
    )

    id_usuario = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        doc="Relación con la tabla de Usuarios.",
    )

    usuario = relationship(
        "Usuario", foreign_keys=[id_usuario], doc="Objeto de relación hacia el Usuario."
    )

    def __repr__(self):
        """Retorna una representación legible del servicio."""
        return f"<Servicio(nombre='{self.nombre}', costo={self.costo_base})>"
