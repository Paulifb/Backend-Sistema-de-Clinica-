import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Medico(Base):
    """Profesionales médicos registrados."""

    __tablename__ = "medicos"

    id_medico = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_especialidad = Column(
        UUID(as_uuid=True), ForeignKey("especialidades.id_especialidad"), nullable=False
    )
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    registro_medico = Column(String(100), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    especialidad = relationship("Especialidad", foreign_keys=[id_especialidad])

    def __repr__(self):
        return f"<Medico(nombre='{self.nombre}', registro='{self.registro_medico}')>"
