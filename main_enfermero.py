import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.crud import crud_enfermero as crud_enfermero
from src.crud import crud_historial as crud_historial
from src.crud import crud_usuario as crud_usuario
from src.entities.usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    """Lee una entrada de texto y elimina espacios."""
    s = input(mensaje).strip()
    return s if s else default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    """Convierte una entrada de texto en UUID."""
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """Gestiona el acceso inicial y registro de usuarios."""
    if not crud_usuario.hay_usuarios():
        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")
        if nombre and contra:
            try:
                crud_usuario.crear(
                    nombre_usuario=nombre, contrasena=contra, rol="admin"
                )
            except Exception:
                return None

    while True:
        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")
        usuario = crud_usuario.login(nombre, contra)
        if usuario:
            return usuario


def menu_enfermero(usuario: Usuario) -> None:
    """Interfaz de consola para operaciones de enfermería."""
    while True:
        print("\n--- MODULO ENFERMERO ---")
        print("1. Listar  2. Registrar  3. Actualizar Historial  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            break
        elif op == "1":
            for e in crud_enfermero.obtener_todos():
                print(f"{e.id_enfermero} | {e.nombre} | {e.area}")
        elif op == "2":
            try:
                crud_enfermero.crear_enfermero(
                    leer_texto("Nombre: "),
                    leer_texto("Teléfono: "),
                    leer_texto("Área: "),
                    leer_texto("Turno: "),
                    usuario.id_usuario,
                )
            except Exception as e:
                print(f"Error: {e}")
        elif op == "3":
            id_h = leer_uuid("ID historial: ")
            if id_h:
                try:
                    crud_historial.actualizar(
                        id_h, observaciones_enfermeria=leer_texto("Observaciones: ")
                    )
                except Exception as e:
                    print(f"Error: {e}")


def main() -> None:
    """Punto de entrada principal del sistema."""
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        return

    while True:
        print(f"\nSISTEMA - Usuario: {usuario.nombre_usuario}")
        print("1. Enfermería  0. Salir")
        op = leer_texto("Opción: ")

        if op == "0":
            break
        elif op == "1":
            menu_enfermero(usuario)


if __name__ == "__main__":
    main()
