from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.crud import crud_usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


class UsuarioCreate(BaseModel):
    nombre_completo: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    clave: str = Field(..., min_length=6)
    rol: str
    estado: str


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    clave: Optional[str] = Field(None, min_length=6)
    rol: Optional[str] = None
    estado: Optional[str] = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre_completo: str
    email: EmailStr
    rol: str
    estado: str


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> List[UsuarioRead]:
    return crud_usuario.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID, db: Session = Depends(get_db)) -> UsuarioRead:
    u = crud_usuario.obtener_por_id(db, id_usuario)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return u


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(body: UsuarioCreate, db: Session = Depends(get_db)) -> UsuarioRead:
    u = crud_usuario.crear_usuario(
        db,
        nombre_completo=body.nombre_completo,
        email=str(body.email),
        clave=body.clave,
        rol=body.rol,
        estado=body.estado,
    )
    return u


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: UUID, body: UsuarioUpdate, db: Session = Depends(get_db)
) -> UsuarioRead:
    data = body.model_dump(exclude_unset=True)
    if "email" in data and data["email"] is not None:
        data["email"] = str(data["email"])
    u = crud_usuario.actualizar_usuario(db, id_usuario, **data)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: UUID, db: Session = Depends(get_db)) -> None:
    if not crud_usuario.eliminar_usuario(db, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
