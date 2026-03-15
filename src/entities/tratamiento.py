import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, Text, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Tratamiento(Base):
    """Modelo de tratamiento"""

    __tablename__ = "tratamiento"

    id_tratamiento = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_historial = Column(
        UUID(as_uuid=True), ForeignKey("categoria.id_categoria"), nullable=False
    )

    nombre_tratamiento = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    dosis = Column(Float, nullable=False)
    duracion = Column(Integer, nullable=False)

    historial_medico = relationship("Historial_medico", foreign_keys=[id_historial])
