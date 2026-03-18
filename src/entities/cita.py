import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Cita(Base):
    """
    Representa una cita médica registrada en el sistema.

    Este modelo almacena la información relacionada con la programación
    de citas entre pacientes y médicos, incluyendo el servicio solicitado,
    la fecha y hora de la cita, el motivo de la consulta y el estado de la
    cita. También guarda información sobre el usuario que creó o editó
    el registro y las fechas correspondientes.
    """

    __tablename__ = "citas"

    id_cita = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_paciente = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id_paciente"), nullable=False
    )

    id_medico = Column(
        UUID(as_uuid=True), ForeignKey("medicos.id_medico"), nullable=False
    )

    id_servicio = Column(
        UUID(as_uuid=True), ForeignKey("servicios.id_servicio"), nullable=False
    )

    fecha_hora = Column(DateTime(timezone=True), nullable=False)

    motivo = Column(String(200), nullable=False)

    estado = Column(Text, nullable=False)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    id_usuario_edicion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    paciente = relationship("Paciente", foreign_keys=[id_paciente])
    servicio = relationship("Servicio", foreign_keys=[id_servicio])
    medico = relationship("Medico", foreign_keys=[id_medico])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion])
