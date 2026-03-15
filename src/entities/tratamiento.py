import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Tratamiento(Base):
    """Modelo de tratamiento"""

    __tablename__ = "tratamientos"

    id_tratamiento = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_historial = Column(
        UUID(as_uuid=True), ForeignKey("historiales.id_historial"), nullable=False
    )

    nombre_tratamiento = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    dosis = Column(Text, nullable=False)
    duracion = Column(Integer, nullable=False)

    historial = relationship("Historial", foreign_keys=[id_historial])
