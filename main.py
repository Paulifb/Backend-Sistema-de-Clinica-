"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

import datetime
import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.crud import crud_medico as medico
from src.crud import crud_servicio as servicio
from src.crud import crud_especialidad as especialidad
from src.crud import crud_cita as cita
from src.crud import crud_enfermero as enfermero
from src.crud import crud_eps as eps
from src.crud import crud_factura as factura
from src.crud import crud_historial as historial
from src.crud import crud_tratamiento as tratamiento
from src.crud import crud_usuario as usuario
from src.entities.usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """
    Maneja creación del primer usuario y login.
    """

    if not usuario.hay_usuarios():
        print("\n--- No hay usuarios en el sistema ---")
        print("Crea el primer usuario.\n")

        nombre = leer_texto("Nombre completo: ")
        if not nombre:
            print("Campo obligatorio.")
            return None

        email = leer_texto("Correo: ")
        if not email:
            print("Campo obligatorio.")
            return None

        clave = leer_texto("Contraseña: ")
        if not clave:
            print("Campo obligatorio.")
            return None

        rol = leer_texto("Rol (paciente/medico/enfermero): ")
        if not rol:
            print("Campo obligatorio.")
            return None

        try:
            usuario_creado = usuario.crear_usuario(
                nombre_completo=nombre,
                email=email,
                clave=clave,
                rol=rol,
                estado="activo",
            )

            print(f"\nUsuario '{usuario_creado.email}' creado. Inicia sesión.\n")

        except ValueError as e:
            print("Error:", e)
            return None

    while True:
        print("--- Inicio de sesión ---")

        email = leer_texto("Correo: ")
        clave = leer_texto("Contraseña: ")

        if not email or not clave:
            print("Campos obligatorios.\n")
            continue

        try:
            usuario_log = usuario.login_usuario(email, clave)

            if usuario_log:
                print(
                    f"\nBienvenido, {usuario_log.nombre_completo} ({usuario_log.rol}).\n"
                )
                return usuario_log
            else:
                print("Correo o contraseña incorrectos.\n")

        except ValueError as e:
            print("Error:", e)


def menu_citas_paciente(usuario):
    while True:
        print("\n--- CITAS ---")
        print(
            "1. Ver citas  2. Crear cita  3. Actualizar cita  4. Eliminar cita  5. Generar factura  0. Volver"
        )
        op = leer_texto("Opción: ")

        if op == "1":
            citas = cita.obtener_todos()
            for c in citas:
                servicios = servicio.obtener_por_id(c.id_servicio)
                print(f"{c.id_cita} | {servicios.nombre} | {c.fecha_hora} | {c.estado}")

        elif op == "2":
            print("\n-- Crear cita --")

            id_paciente = leer_uuid("Id paciente: ")
            if not id_paciente:
                print("ID inválido")
                continue

            id_medico = leer_uuid("Id medico: ")
            if not id_medico:
                print("ID inválido")
                continue

            print("\n-- Servicios disponibles --")
            for s in servicio.obtener_todos():
                print(f"{s.id_servicio} | {s.nombre}")

            id_servicio = leer_uuid("Id servicio: ")
            if not id_servicio:
                print("ID inválido")
                continue

            fecha = leer_texto("Fecha (YYYY-MM-DD HH:MM): ")
            motivo = leer_texto("Motivo: ")
            estado = leer_texto("Estado (pendiente/confirmada/cancelada): ")

            try:
                fecha_hora = datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M")
                fecha_hora = fecha_hora.replace(tzinfo=datetime.timezone.utc)

                cita.crear_cita(
                    id_paciente=id_paciente,
                    id_medico=id_medico,
                    id_servicio=id_servicio,
                    fecha_hora=fecha_hora,
                    motivo=motivo,
                    estado=estado,
                    id_usuario_creacion=usuario.id_usuario,
                )

                print("Cita creada")

            except ValueError as e:
                print("Error:", e)

        elif op == "3":
            print("\n-- Actualizar cita --")

            id_cita = leer_uuid("Id cita: ")
            if not id_cita:
                print("ID inválido")
                continue

            print("Deja vacío lo que no quieras cambiar")

            nueva_fecha = leer_texto("Nueva fecha (YYYY-MM-DD HH:MM): ")
            nuevo_motivo = leer_texto("Nuevo motivo: ")
            nuevo_estado = leer_texto("Nuevo estado: ")

            datos = {}

            if nueva_fecha:
                try:
                    fecha_hora = datetime.datetime.strptime(
                        nueva_fecha, "%Y-%m-%d %H:%M"
                    )
                    fecha_hora = fecha_hora.replace(tzinfo=datetime.timezone.utc)
                    datos["fecha_hora"] = fecha_hora
                except ValueError:
                    print("Formato de fecha inválido")
                    continue

            if nuevo_motivo:
                datos["motivo"] = nuevo_motivo

            if nuevo_estado:
                datos["estado"] = nuevo_estado

            try:
                actualizado = cita.actualizar_cita(
                    id_cita=id_cita,
                    id_usuario_edicion=usuario.id_usuario,
                    **datos,
                )

                if actualizado:
                    print("Cita actualizada")
                else:
                    print("Cita no encontrada")

            except ValueError as e:
                print("Error:", e)

        elif op == "4":
            print("\n-- Generar factura --")

            id_cita = leer_uuid("ID cita: ")
            if not id_cita:
                print("ID inválido")
                continue

            citas = cita.obtener_por_id(id_cita)
            if not citas:
                print("La cita no existe")
                continue

            if citas.id_paciente != usuario.id_usuario:
                print("No puedes generar factura de esta cita")
                continue

            facturas = factura.obtener_todos()
            if any(f.id_cita == id_cita for f in facturas):
                print("Ya existe factura para esta cita")
                continue

            servicios = servicio.obtener_por_id(cita.id_servicio)

            if not servicio:
                print("Servicio no encontrado")
                continue

            total = servicio.precio

            estado_pago = leer_texto("Estado de pago (Pendiente/Pagado/Cancelado): ")
            metodo_pago = leer_texto(
                "Método de pago (Efectivo/Tarjeta/Transferencia): "
            )

            try:
                factura.crear_factura(
                    id_cita=id_cita,
                    total=total,
                    estado_pago=estado_pago,
                    fecha_pago=datetime.now(datetime.timezone.utc),
                    id_usuario_creacion=usuario.id_usuario,
                    metodo_pago=metodo_pago if metodo_pago else None,
                )

                print("Factura generada correctamente")

            except ValueError as e:
                print("Error:", e)

        elif op == "0":
            break


def menu_medico(usuario):
    while True:
        print("\n--- MEDICO ---")
        print(
            "1. Ver citas  2. Historial medico  3. Ver medicos  4. Registrar medico 5. Actualizar medico 6. Eliminar medico 0. Volver"
        )
        op = leer_texto("Opción: ")

        if op == "1":
            citas = cita.obtener_todos()
            for p in citas:
                if p.id_medico == usuario.id_usuario:
                    servicios = servicio.obtener_por_id(p.id_servicio)
                    print(f"{p.id_cita} | {servicios.nombre} | {p.fecha_hora}")

        elif op == "2":
            menu_historial(usuario)

        elif op == "3":
            medicos = medico.obtener_todos_medicos()
            for m in medicos:
                espe = especialidad.obtener_por_id(m.id_especialidad)
                print(f"{m.id_medico} | {espe.nombre}")

        elif op == "4":
            print("\n-- Especialidades--")
            for e in especialidad.obtener_todas():
                print(f"{e.id_especialidad} | {e.nombre}")

            id_usuario = leer_uuid("Id usuario: ")
            if not id_usuario:
                print("ID inválido")
                continue

            id_especialidad = leer_uuid("Id especialidad: ")
            if not id_especialidad:
                print("ID inválido")
                continue

            try:
                medico.crear_medico(
                    id_usuario=id_usuario,
                    id_especialidad=id_especialidad,
                )
                print("Médico creado")

            except ValueError as e:
                print("Error:", e)

        elif op == "5":
            id_medico = leer_uuid("Id medico: ")

            if not id_medico:
                print("ID inválido")
                continue

            print("\n-- Especialidades--")
            for e in especialidad.obtener_todas():
                print(f"{e.id_especialidad} | {e.nombre}")

            id_especialidad = leer_uuid("Nueva especialidad: ")
            if not id_especialidad:
                print("ID inválido")
                continue

            try:
                actualizado = medico.actualizar_medico(
                    id_medico, id_especialidad=id_especialidad
                )

                if actualizado:
                    print("Médico actualizado")
                else:
                    print("Médico no encontrado")

            except ValueError as e:
                print("Error:", e)

        elif op == "6":
            id_medico = leer_uuid("Id medico: ")
            if not id_medico:
                print("ID inválido")
                continue

            eliminado = medico.eliminar_medico(id_medico)

            if eliminado:
                print("Médico eliminado")
            else:
                print("Médico no encontrado")

        elif op == "0":
            break


def menu_historial(usuario):
    while True:
        print("\n--- Historial Medico ---")
        print(
            "1. Ver  2. Crear Historial medico  3. Editar  4. Eliminar 5. Tratamientos 0. Volver"
        )
        op = leer_texto("Opción: ")

        if op == "1":
            for h in historial.obtener_todos():
                print(h)

        elif op == "2":
            id_cita = leer_uuid("Id de la cita: ")
            if not id_cita:
                print("ID inválido")
                continue

            id_enfermero = leer_uuid("Id enfermero: ")
            if not id_enfermero:
                print("ID inválido")
                continue

            diagnostico = leer_texto("Diagnostico: ")
            if not diagnostico:
                print("Campo obligatorio")
                continue

            try:
                historial.crear_historial(
                    id_cita=id_cita,
                    id_enfermero=id_enfermero,
                    diagnostico=diagnostico,
                    observaciones_medicas=leer_texto("Obs médicas: "),
                    indicaciones_enfermeria=leer_texto("Indicaciones enfermería: "),
                    observaciones_enfermeria=leer_texto("Obs enfermería: "),
                    id_usuario_creacion=usuario.id_usuario,
                )
                print("Historial creado")

            except ValueError as e:
                print("Error:", e)

        elif op == "3":
            id_historial = leer_uuid("Id historial: ")
            if not id_historial:
                print("ID inválido")
                continue

            diagnostico = leer_texto("Nuevo diagnostico: ")
            if not diagnostico:
                print("Campo obligatorio")
                continue

            try:
                actualizado = historial.actualizar_historial(
                    id_historial=id_historial,
                    id_usuario_edicion=usuario.id_usuario,
                    diagnostico=diagnostico,
                )

                if actualizado:
                    print("Historial actualizado")
                else:
                    print("Historial no encontrado")

            except ValueError as e:
                print("Error:", e)

        elif op == "4":
            id_historial = leer_uuid("Id historial: ")
            if not id_historial:
                print("ID inválido")
                continue

            eliminado = historial.eliminar_historial(id_historial)

            if eliminado:
                print("Historial eliminado")
            else:
                print("Historial no encontrado")

        elif op == "5":
            menu_tratamientos()

        elif op == "0":
            break


def menu_tratamientos(usuario):
    while True:
        print("\n--- Historial Medico ---")
        print("1. Ver  2. Crear tratamiento  3. Editar  4. Eliminar 0. Volver")
        op = leer_texto("Opción: ")

        if op == "1":
            for t in tratamiento.obtener_todos():
                print(t)

        elif op == "2":
            id_historial = leer_uuid("Id historial medico: ")

            if not id_historial:
                print("ID inválido")
                continue

            nombre = leer_texto("Nombre del tratamiento: ")
            if not nombre:
                print("Campo obligatorio")
                continue

            try:
                tratamiento.crear(
                    id_historial=id_historial,
                    nombre_tratamiento=nombre,
                    dosis=leer_texto("Dosis: "),
                    duracion=leer_texto("Duración: "),
                )
                print("Tratamiento creado")

            except ValueError as e:
                print("Error:", e)

        elif op == "3":
            id_tratamiento = leer_uuid("Id tratamiento: ")
            if not id_tratamiento:
                print("ID inválido")
                continue

            nombre = leer_texto("Nuevo nombre: ")
            if not nombre:
                print("Campo obligatorio")
                continue

            try:
                actualizado = tratamiento.actualizar(
                    id_tratamiento=id_tratamiento,
                    nombre_tratamiento=nombre,
                )

                if actualizado:
                    print("Tratamiento actualizado")
                else:
                    print("Tratamiento no encontrado")

            except ValueError as e:
                print("Error:", e)

        elif op == "4":
            id_tratamiento = leer_uuid("Id tratamiento: ")
            if not id_tratamiento:
                print("ID inválido")
                continue

            eliminado = tratamiento.eliminar(id_tratamiento)

            if eliminado:
                print("Tratamiento eliminado")
            else:
                print("Tratamiento no encontrado")

        elif op == "0":
            break


def menu_enfermero(usuario: Usuario) -> None:
    """Interfaz de consola para operaciones de enfermería."""
    while True:
        print("\n--- MODULO ENFERMERO ---")
        print("1. Listar  2. Registrar  3. Actualizar Historial  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            break
        elif op == "1":
            for e in enfermero.obtener_todos():
                print(f"{e.id_enfermero} | {e.nombre} | {e.area}")
        elif op == "2":
            try:
                enfermero.crear_enfermero(
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
                    historial.actualizar(
                        id_h, observaciones_enfermeria=leer_texto("Observaciones: ")
                    )
                except Exception as e:
                    print(f"Error: {e}")


def main() -> None:
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print("1. Continuar  0. Salir")

        op = leer_texto("Opción: ")

        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break

        if usuario.rol == "paciente":
            menu_paciente(usuario)

        elif usuario.rol == "medico":
            menu_medico(usuario)

        elif op == "enfermero":
            menu_enfermero(usuario)

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
