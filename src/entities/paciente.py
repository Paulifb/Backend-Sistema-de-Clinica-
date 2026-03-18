import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Paciente(Base):
    """Modelo de base de datos para los pacientes."""

    __tablename__ = "pacientes"

    id_paciente = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    diagnostico = Column(String(255), nullable=True)
    correo = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)

    def __repr__(self):
        return f"<Paciente(nombre='{self.nombre}', correo='{self.correo}')>"
