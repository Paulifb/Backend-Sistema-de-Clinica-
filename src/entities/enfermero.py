import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Enfermero(Base):
    """
    Representa a un enfermero registrado en el sistema.

    Este modelo almacena la información básica de los enfermeros,
    incluyendo su nombre completo, teléfono, área de trabajo y
    turno asignado. También mantiene la relación con el usuario
    asociado dentro del sistema.
    """

    __tablename__ = "enfermeros"

    id_enfermero = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    nombre = Column(String(120), nullable=False)

    telefono = Column(String(20), nullable=False)

    area = Column(String(120), nullable=False)

    turno = Column(String(120), nullable=False)

    usuario = relationship("Usuario", foreign_keys=[id_usuario])
