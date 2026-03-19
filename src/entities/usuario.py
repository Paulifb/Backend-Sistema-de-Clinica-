from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, String, func
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
    estado = Column(String(100), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())


class PersonaBase(BaseModel):
    """Esquema base con validaciones simples."""

    nombre: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    activo: bool = True


class PersonaCreate(PersonaBase):
    """Esquema para creación."""

    pass


class PersonaUpdate(BaseModel):
    """Esquema para actualización parcial."""

    nombre_usuario: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class PersonaResponse(PersonaBase):
    """Esquema de respuesta (lectura)."""

    id_usuario: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None  # type: ignore

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}
