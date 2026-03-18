import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Especialidad(Base):
    """Especialidades médicas disponibles."""

    __tablename__ = "especialidades"

    id_especialidad = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Especialidad(nombre='{self.nombre}')>"
