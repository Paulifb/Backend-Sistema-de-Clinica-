import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Eps(Base):
    """Modelo de EPS del sistema"""

    __tablename__ = "eps"

    id_eps = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=True)
