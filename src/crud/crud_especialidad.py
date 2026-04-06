from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.entities.especialidad import Especialidad
from src.entities.usuario import Usuario


def obtener_especialidad_por_id(
    db: Session, id_especialidad: UUID
) -> Optional[Especialidad]:
    """Busca una especialidad específica por su identificador único."""
    return (
        db.query(Especialidad)
        .filter(Especialidad.id_especialidad == id_especialidad)
        .first()
    )


def obtener_todas_especialidades(db: Session) -> List[Especialidad]:
    """Obtiene el listado completo de especialidades registradas."""
    return db.query(Especialidad).all()


def crear_especialidad(
    db: Session, nombre: str, id_usuario: UUID, descripcion: Optional[str] = None
) -> Especialidad:
    """
    Registra una nueva especialidad en la base de datos.

    Valida que el nombre no esté vacío y que el usuario responsable exista.
    """
    nombre = nombre.strip().capitalize()
    if not nombre:
        raise ValueError("El nombre de la especialidad no puede estar vacío")

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    nueva = Especialidad(nombre=nombre, descripcion=descripcion, id_usuario=id_usuario)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def actualizar_especialidad(
    db: Session, id_especialidad: UUID, id_usuario: UUID, **kwargs
) -> Optional[Especialidad]:
    """
    Modifica los datos de una especialidad existente de forma dinámica.

    Verifica la existencia del registro y del usuario que realiza la edición.
    Solo permite modificar campos permitidos como nombre y descripción.
    """
    especialidad = obtener_especialidad_por_id(db, id_especialidad)
    if not especialidad:
        return None

    if not db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
        raise ValueError("El usuario especificado no existe")

    campos_validos = {"nombre", "descripcion"}
    for key, value in kwargs.items():
        if key in campos_validos:
            if key == "nombre":
                value = value.strip().capitalize()
                if not value:
                    raise ValueError("El nombre no puede estar vacío")
            setattr(especialidad, key, value)

    especialidad.id_usuario = id_usuario
    db.commit()
    db.refresh(especialidad)
    return especialidad


def eliminar_especialidad(db: Session, id_especialidad: UUID) -> bool:
    """
    Elimina una especialidad de la base de datos tras verificar su existencia.

    Retorna True si se eliminó correctamente, de lo contrario retorna False.
    """
    especialidad = obtener_especialidad_por_id(db, id_especialidad)
    if especialidad:
        db.delete(especialidad)
        db.commit()
        return True
    return False
