import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Usuario(Base):
    """
    Representa un usuario registrado en el sistema.

    Este modelo almacena la información básica de los usuarios,
    incluyendo su nombre completo, correo electrónico, clave de
    acceso, rol dentro del sistema y su estado.
    """

    __tablename__ = "usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_completo = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    clave = Column(String(120), nullable=False)
    rol = Column(String(50), nullable=False)
    estado = Column(Text, default=True)
