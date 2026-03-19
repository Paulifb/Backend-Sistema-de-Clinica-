import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Paciente(Base):
    """Modelo de paciente"""

    __tablename__ = "pacientes"

    id_paciente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_eps = Column(UUID(as_uuid=True), ForeignKey("eps.id_eps"), nullable=False)

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(DateTime, nullable=False)
    direccion = Column(String(200), nullable=True)
    genero = Column(String(20), nullable=False)
    tipo_afiliacion = Column(String(50), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edicion])
    eps = relationship("Eps", foreign_keys=[id_eps])
    usuario = relationship("Usuario", foreign_keys=[id_usuario])
