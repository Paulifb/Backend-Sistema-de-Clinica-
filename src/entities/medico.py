import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Medico(Base):
    """
    Representa a los profesionales médicos registrados en el sistema.

    Esta clase vincula la información de contacto y profesional del médico
    con su especialidad y su cuenta de usuario.
    """

    __tablename__ = "medicos"

    id_medico = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        doc="Identificador único del médico (Primary Key).",
    )

    id_usuario = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        doc="Relación con la tabla de Usuarios.",
    )

    id_especialidad = Column(
        UUID(as_uuid=True),
        ForeignKey("especialidades.id_especialidad"),
        nullable=False,
        doc="Relación con la tabla de Especialidades.",
    )

    nombre = Column(
        String(100), nullable=False, doc="Nombre completo del profesional médico."
    )

    telefono = Column(
        String(20), nullable=True, doc="Número de teléfono de contacto del médico."
    )

    registro_medico = Column(
        String(100),
        nullable=True,
        doc="Número de registro o licencia médica profesional.",
    )

    # RELACIONES
    usuario = relationship(
        "Usuario", foreign_keys=[id_usuario], doc="Objeto de relación hacia el Usuario."
    )

    especialidad = relationship(
        "Especialidad",
        foreign_keys=[id_especialidad],
        doc="Objeto de relación hacia la Especialidad.",
    )

    def __repr__(self):
        """Retorna una representación legible del médico."""
        return f"<Medico(nombre='{self.nombre}', registro='{self.registro_medico}')>"
