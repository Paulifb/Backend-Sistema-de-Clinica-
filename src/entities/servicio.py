import uuid
from sqlalchemy import Column, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Servicio(Base):
    """Servicios médicos o procedimientos ofrecidos."""

    __tablename__ = "servicios"

    id_servicio = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    costo_base = Column(Float, nullable=False)
    duracion_aproximada = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Servicio(nombre='{self.nombre}', costo={self.costo_base})>"
