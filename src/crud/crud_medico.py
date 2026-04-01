from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.medico import Medico
from src.entities.usuario import Usuario
from src.entities.especialidad import Especialidad


def obtener_medico_por_id(db: Session, id_medico: UUID) -> Optional[Medico]:
    """Busca un médico en la base de datos mediante su ID único."""
    return db.query(Medico).filter(Medico.id_medico == id_medico).first()


def obtener_todos_medicos(db: Session) -> List[Medico]:
    """Recupera el listado completo de todos los médicos registrados."""
    return db.query(Medico).all()


def crear_medico(
    db: Session,
    nombre: str,
    id_usuario: UUID,
    id_especialidad: UUID,
    telefono: Optional[str] = None,
) -> Medico:
    """Registra un nuevo médico validando la existencia del usuario y la especialidad."""
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El nombre del médico no puede estar vacío")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    if (
        not db.query(Especialidad)
        .filter(Especialidad.id_especialidad == id_especialidad)
        .first()
    ):
        raise ValueError("La especialidad especificada no existe")

    nuevo = Medico(
        nombre=nombre,
        id_usuario=id_usuario,
        id_especialidad=id_especialidad,
        telefono=telefono,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def actualizar_medico(
    db: Session,
    id_medico: UUID,
    id_usuario: UUID,
    **kwargs,
) -> Optional[Medico]:
    """Actualiza los datos de un médico (nombre, teléfono o especialidad) de forma dinámica."""
    medico = obtener_medico_por_id(db, id_medico)
    if not medico:
        return None

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario que realiza la edición no existe")

    campos_validos = {"nombre", "telefono", "id_especialidad"}
    for key, value in kwargs.items():
        if key in campos_validos:
            if isinstance(value, str):
                value = value.strip()

            if key == "nombre" and not value:
                raise ValueError("El nombre no puede estar vacío")

            if key == "id_especialidad":
                if (
                    not db.query(Especialidad)
                    .filter(Especialidad.id_especialidad == value)
                    .first()
                ):
                    raise ValueError("La nueva especialidad no existe")

            setattr(medico, key, value)

    medico.id_usuario = id_usuario
    db.commit()
    db.refresh(medico)
    return medico


def eliminar_medico(db: Session, id_medico: UUID) -> bool:
    """Elimina el registro de un médico si este existe en la base de datos."""
    medico = obtener_medico_por_id(db, id_medico)
    if medico:
        db.delete(medico)
        db.commit()
        return True
    return False
