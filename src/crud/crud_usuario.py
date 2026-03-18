"""
CRUD para la entidad Usuario.
Incluye creacion, login (verificacion de contraseña) y operaciones basicas.
"""

import hashlib
from typing import List, Optional, Text
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.usuario import Usuario


def _hash_clave(clave: str) -> str:
    """
    Hashea la contraseña utilizando SHA-256.

    Args:
        clave: Contraseña en texto plano.

    Returns:
        Contraseña hasheada.
    """
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def crear_usuario(
    nombre_completo: str,
    email: str,
    clave: str,
    rol: str,
    estado: Text,
) -> Usuario:
    """
    Crea un nuevo usuario en el sistema.

    Args:
        nombre_completo: Nombre completo del usuario.
        email: Correo electrónico del usuario.
        clave: Contraseña del usuario. será hasheada antes de almacenarse.
        rol: Rol del usuario.
        estado: Estado del usuario.

    Returns:
        El usuario creado.
    """
    db = SessionLocal()

    nombre_completo = nombre_completo.strip()
    email = email.strip().lower()
    rol = rol.strip().lower()
    estado = estado.strip().lower()

    if not nombre_completo:
        raise ValueError("El nombre completo no puede estar vacío")

    if not email:
        raise ValueError("El correo electrónico no puede estar vacío")

    if not clave.strip():
        raise ValueError("La contraseña no puede estar vacía")

    if rol not in ["paciente", "medico", "enfermero"]:
        raise ValueError("El rol no es válido")

    if estado not in ["activo", "inactivo"]:
        raise ValueError("El estado no es válido")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is not None:
        raise ValueError("El correo electrónico ya está registrado")

    usuario = Usuario(
        nombre_completo=nombre_completo,
        email=email,
        clave=_hash_clave(clave),
        rol=rol,
        estado=estado,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def login_usuario(email: str, clave: str) -> Optional[Usuario]:
    """
    Verifica las credenciales de un usuario para iniciar sesión.

    Args:
        email: Correo electrónico del usuario.
        clave: Contraseña del usuario.

    Returns:
        El usuario si las credenciales son correctas, o None si son incorrectas.
    """

    usuario = obtener_por_email(email)

    if not usuario:
        return None

    if usuario.estado != "activo":
        raise ValueError("El usuario no está activo")

    if usuario.clave != _hash_clave(clave):
        return None

    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    """
    Obtiene un usuario por su identificador.
    """
    db = SessionLocal()

    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_email(email: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su correo electrónico.
    """
    db = SessionLocal()

    email = email.strip().lower()

    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_todos() -> List[Usuario]:
    """
    Obtiene todos los usuarios.
    """
    db = SessionLocal()

    return db.query(Usuario).all()


def hay_usuarios() -> bool:
    """
    Verifica si hay usuarios registrados.
    """
    db = SessionLocal()

    return db.query(Usuario).first() is not None


def actualizar_usuario(
    id_usuario: UUID,
    args: dict,
) -> Optional[Usuario]:
    """
    Actualiza los campos de un usuario existente.

    Args:
        id_usuario: Identificador del usuario a actualizar.
        args: Diccionario con los campos y valores a actualizar.

    Returns:
        El usuario actualizado o None si el usuario no existe.
    """
    db = SessionLocal()

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if not usuario:
        return None

    campos_validos = {"nombre_completo", "email", "clave", "rol", "estado"}

    for key, value in args.items():

        if key not in campos_validos:
            continue

        if isinstance(value, str):
            value = value.strip()

        if key == "nombre_completo" and not value:
            raise ValueError("El nombre no puede estar vacio")

        if key == "rol" and value.lower() not in ["paciente", "medico", "enfermero"]:
            raise ValueError("El rol no es válido")

        if key == "estado" and value.lower() not in ["activo", "inactivo"]:
            raise ValueError("El estado no es válido")

        if key == "email":
            value = value.lower()
            usuario_existente = db.query(Usuario).filter(Usuario.email == value).first()
            if usuario_existente and usuario_existente.id_usuario != id_usuario:
                raise ValueError("El correo electrónico ya está registrado")

        if key == "clave":
            value = _hash_clave(value)

        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return usuario


def eliminar_usuario(id_usuario: UUID) -> bool:
    """
    Elimina un usuario por su identificador.
    """

    db = SessionLocal()

    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    if usuario:
        db.delete(usuario)
        db.commit()
        return True

    return False
