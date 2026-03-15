import uuid

from sqlalchemy import Column, DateTime, Float, Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Factura(Base):
    """Modelo de Factura"""

    __tablename__ = "factura"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_cita = Column(UUID(as_uuid=True), ForeignKey("cita.id_cita"), nullable=False)

    total = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=True)
    estado_pago = Column(Boolean, nullable=False)
    fecha_pago = Column(DateTime, nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    cita = relationship("Cita", foreign_keys=[id_cita])
