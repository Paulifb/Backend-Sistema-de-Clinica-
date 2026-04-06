from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .deps import DbSession
from src.crud import crud_usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


class UsuarioCreate(BaseModel):
    """
    Esquema para la creación de un usuario.

    Attributes:
        nombre_completo: Nombre completo del usuario.
        email: Correo electrónico del usuario.
        clave: Contraseña del usuario (mínimo 6 caracteres).
        rol: Rol asignado al usuario (paciente, medico, enfermero).
        estado: Estado del usuario (activo o inactivo).
    """

    nombre_completo: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    clave: str = Field(..., min_length=6)
    rol: str
    estado: str


class UsuarioUpdate(BaseModel):
    """
    Esquema para la actualización de un usuario.

    Todos los campos son opcionales y solo se actualizarán
    los que sean enviados en la petición.

    Attributes:
        nombre_completo: Nuevo nombre del usuario.
        email: Nuevo correo electrónico.
        clave: Nueva contraseña.
        rol: Nuevo rol del usuario.
        estado: Nuevo estado del usuario.
    """

    nombre_completo: Optional[str] = Field(None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    clave: Optional[str] = Field(None, min_length=6)
    rol: Optional[str] = None
    estado: Optional[str] = None


class UsuarioRead(BaseModel):
    """
    Esquema de lectura de un usuario.

    Representa la información que se devuelve al cliente,
    excluyendo datos sensibles como la contraseña.

    Attributes:
        id_usuario: Identificador único del usuario.
        nombre_completo: Nombre completo del usuario.
        email: Correo electrónico del usuario.
        rol: Rol asignado.
        estado: Estado actual del usuario.
    """

    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre_completo: str
    email: EmailStr
    rol: str
    estado: str


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(
    db: DbSession, skip: int = 0, limit: int = 100
) -> List[UsuarioRead]:
    """
    Obtiene una lista de usuarios con paginación.

    Args:
        db: Sesión de base de datos.
        skip: Número de registros a omitir.
        limit: Número máximo de registros a retornar.

    Returns:
        Lista de usuarios.
    """
    return crud_usuario.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID, db: DbSession) -> UsuarioRead:
    """
    Obtiene un usuario por su identificador.

    Args:
        id_usuario: Identificador del usuario.
        db: Sesión de base de datos.

    Returns:
        Usuario encontrado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    u = crud_usuario.obtener_por_id(db, id_usuario)

    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return u


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioCreate, db: DbSession) -> UsuarioRead:
    """
    Crea un nuevo usuario.

    Args:
        body: Datos del usuario a crear.
        db: Sesión de base de datos.

    Returns:
        Usuario creado.

    Raises:
        HTTPException: Si ocurre un error de validación.
    """
    try:
        u = crud_usuario.crear_usuario(
            db,
            nombre_completo=body.nombre_completo,
            email=str(body.email),
            clave=body.clave,
            rol=body.rol,
            estado=body.estado,
        )
        return u

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: UUID, body: UsuarioUpdate, db: DbSession
) -> UsuarioRead:
    """
    Actualiza un usuario existente.

    Args:
        id_usuario: Identificador del usuario.
        body: Datos a actualizar.
        db: Sesión de base de datos.

    Returns:
        Usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe o hay errores de validación.
    """
    try:
        data = body.model_dump(exclude_unset=True)

        if "email" in data and data["email"] is not None:
            data["email"] = str(data["email"])

        u = crud_usuario.actualizar_usuario(db, id_usuario, **data)

        if not u:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return u

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: UUID, db: DbSession) -> None:
    """
    Elimina un usuario por su identificador.

    Args:
        id_usuario: Identificador del usuario.
        db: Sesión de base de datos.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    if not crud_usuario.eliminar_usuario(db, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
