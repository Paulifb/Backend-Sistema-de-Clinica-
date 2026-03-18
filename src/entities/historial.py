import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Historial(Base):
    """
    Modelo de historial medico

    Contiene el diagnóstico del paciente, observaciones médicas,
    indicaciones y observaciones de enfermería, así como la
    información de creación y edición del registro.
    """

    __tablename__ = "historiales"

    id_historial = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_cita = Column(UUID(as_uuid=True), ForeignKey("citas.id_cita"), nullable=False)

    id_enfermero = Column(
        UUID(as_uuid=True), ForeignKey("enfermeros.id_enfermero"), nullable=False
    )

    diagnostico = Column(String(255), nullable=False)

    observaciones_medicas = Column(String(200), nullable=True)
    indicaciones_enfermeria = Column(String(200), nullable=True)
    observaciones_enfermeria = Column(String(200), nullable=True)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    cita = relationship("Cita", foreign_keys=[id_cita])
    enfermero = relationship("Enfermero", foreign_keys=[id_enfermero])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion])
