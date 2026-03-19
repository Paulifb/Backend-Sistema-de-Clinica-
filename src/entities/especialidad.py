import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Especialidad(Base):
    """
    Representa las áreas médicas o especialidades disponibles en el sistema.

    Esta entidad funciona como un catálogo maestro de datos predefinidos
    que no requieren seguimiento de auditoría ni edición frecuente.
    """

    __tablename__ = "especialidades"

    id_especialidad = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Identificador único universal de la especialidad.",
    )

    nombre = Column(
        String(100),
        nullable=False,
        doc="Nombre de la especialidad (ej. Cardiología, Pediatría).",
    )

    descripcion = Column(
        Text,
        nullable=True,
        doc="Descripción detallada de lo que abarca la especialidad.",
    )

    def __repr__(self):
        """Retorna una representación legible del objeto Especialidad."""
        return f"<Especialidad(nombre='{self.nombre}')>"
