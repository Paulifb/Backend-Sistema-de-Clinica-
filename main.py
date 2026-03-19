"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

from datetime import datetime, timezone
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
from src.crud import crud_paciente as paciente
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
        print("\n1. Iniciar sesión  2. Crear usuario  0. Salir")
        op = leer_texto("Opción: ")

        if op == "1":
            email = leer_texto("Correo: ")
            clave = leer_texto("Contraseña: ")

            if not email or not clave:
                print("Campos obligatorios.\n")
                continue

            usuario_log = usuario.login_usuario(email, clave)

            if usuario_log:
                print(
                    f"\nBienvenido, {usuario_log.nombre_completo} ({usuario_log.rol}).\n"
                )
                return usuario_log
            else:
                print("Correo o contraseña incorrectos.\n")

        elif op == "2":
            try:
                nombre = leer_texto("Nombre completo: ")
                email = leer_texto("Correo: ")
                clave = leer_texto("Contraseña: ")
                rol = leer_texto("Rol (paciente/medico/enfermero): ")

                nuevo = usuario.crear_usuario(
                    nombre_completo=nombre,
                    email=email,
                    clave=clave,
                    rol=rol,
                    estado="activo",
                )

                print(f"Usuario {nuevo.email} creado correctamente.\n")

            except Exception as e:
                print("Error:", e)

        elif op == "0":
            return None


def menu_paciente(usuario):
    while True:
        print("\n--- PACIENTE ---")
        print(
            "1. Ver mi perfil  2. Registrar datos de paciente  3. Listar todos  4. Ver EPS disponibles  5. Actualizar mis datos  6. Eliminar mi perfil 7. Agendar cita 0. Volver"
        )
        op = leer_texto("Opción: ")

        if op == "1":
            encontrado = False
            for p in paciente.obtener_todos():
                if p.id_usuario == usuario.id_usuario:
                    eps_obj = eps.obtener_por_id(p.id_eps)
                    nombre_eps = eps_obj.nombre if eps_obj else "Sin EPS"
                    print(
                        f"ID: {p.id_paciente} | Nombre: {p.nombre} | EPS: {nombre_eps}"
                    )
                    encontrado = True
            if not encontrado:
                print("No se encontró perfil registrado.")

        elif op == "2":
            try:
                nombre = leer_texto("Nombre: ")
                if not nombre:
                    print("Nombre obligatorio")
                    continue

                fecha_nac_str = leer_texto("Fecha nacimiento (AAAA-MM-DD): ")
                if not fecha_nac_str:
                    print("Fecha obligatoria")
                    continue

                fecha_nacimiento = datetime.strptime(fecha_nac_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )

                nombre_eps = leer_texto("Nombre de la EPS: ")
                telefono_eps = leer_texto("Teléfono EPS: ")
                direccion_eps = leer_texto("Dirección EPS: ")

                if not nombre_eps or not telefono_eps or not direccion_eps:
                    print("Todos los datos de la EPS son obligatorios")
                    continue

                lista_eps = eps.obtener_todos()
                eps_encontrada = None

                for e in lista_eps:
                    if e.nombre.lower() == nombre_eps.lower():
                        eps_encontrada = e
                        break

                if not eps_encontrada:
                    eps_encontrada = eps.crear_eps(
                        nombre=nombre_eps,
                        telefono=telefono_eps,
                        direccion=direccion_eps,
                    )

                paciente.crear_paciente(
                    nombre=nombre,
                    fecha_nacimiento=fecha_nacimiento,
                    genero=leer_texto("Género: "),
                    tipo_afiliacion=leer_texto("Tipo afiliación: "),
                    id_eps=eps_encontrada.id_eps,
                    id_usuario=usuario.id_usuario,
                    id_usuario_creacion=usuario.id_usuario,
                    telefono=leer_texto("Teléfono: "),
                    direccion=leer_texto("Dirección: "),
                )

                print("Datos registrados exitosamente.")

            except Exception as e:
                print("Error:", e)

        elif op == "3":
            for p in paciente.obtener_todos():
                eps_obj = eps.obtener_por_id(p.id_eps)
                nombre_eps = eps_obj.nombre if eps_obj else "Sin EPS"
                print(
                    f"{p.id_paciente} | {p.nombre} | {p.tipo_afiliacion} | {nombre_eps}"
                )

        elif op == "4":
            lista_eps = eps.obtener_todos()
            if not lista_eps:
                print("No hay EPS registradas.")
            else:
                print("\n--- EPS DISPONIBLES ---")
                for e in lista_eps:
                    print(f"{e.id_eps} | {e.nombre} | {e.telefono}")

        elif op == "5":
            paciente_encontrado = None

            for p in paciente.obtener_todos():
                if p.id_usuario == usuario.id_usuario:
                    paciente_encontrado = p
                    break

            if not paciente_encontrado:
                print("No tienes perfil registrado.")
                continue

            try:
                print("Deja vacío si no deseas cambiar el dato")

                nuevo_nombre = leer_texto("Nuevo nombre: ")
                nuevo_telefono = leer_texto("Nuevo teléfono: ")
                nueva_direccion = leer_texto("Nueva dirección: ")

                datos_actualizar = {}

                if nuevo_nombre:
                    datos_actualizar["nombre"] = nuevo_nombre
                if nuevo_telefono:
                    datos_actualizar["telefono"] = nuevo_telefono
                if nueva_direccion:
                    datos_actualizar["direccion"] = nueva_direccion

                if not datos_actualizar:
                    print("No se realizaron cambios.")
                    continue

                paciente.actualizar(
                    id_paciente=paciente_encontrado.id_paciente,
                    id_usuario=usuario.id_usuario,
                    **datos_actualizar,
                )

                print("Datos actualizados correctamente.")

            except Exception as e:
                print("Error:", e)

        elif op == "6":
            paciente_encontrado = None

            for p in paciente.obtener_todos():
                if p.id_usuario == usuario.id_usuario:
                    paciente_encontrado = p
                    break

            if not paciente_encontrado:
                print("No tienes perfil registrado.")
                continue

            confirmacion = leer_texto("¿Seguro que deseas eliminar tu perfil? (s/n): ")

            if confirmacion.lower() == "s":
                eliminado = paciente.eliminar(paciente_encontrado.id_paciente)

                if eliminado:
                    print("Perfil eliminado correctamente.")
                else:
                    print("No se pudo eliminar el perfil.")
            else:
                print("Operación cancelada.")

        elif op == "7":
            menu_citas_paciente(usuario)

        elif op == "0":
            break


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
            lista_servicios = servicio.obtener_todos()

            for s in lista_servicios:
                print(f"{s.id_servicio} | {s.nombre} | ${s.costo_base}")

            nombre_servicio = (
                leer_texto("Servicio (si no existe, se creará): ").strip().lower()
            )

            if not nombre_servicio:
                print("Campo obligatorio")
                continue

            servicio_encontrado = None
            for s in lista_servicios:
                if s.nombre.lower() == nombre_servicio:
                    servicio_encontrado = s
                    break

            if not servicio_encontrado:
                try:
                    costo = leer_float("Costo del nuevo servicio: ")
                    if costo <= 0:
                        print("Costo inválido")
                        continue

                    descripcion = leer_texto("Descripción (opcional): ")
                    duracion = leer_texto("Duración (ej: 30 min) (opcional): ")

                    servicio_encontrado = servicio.crear_servicio(
                        nombre=nombre_servicio,
                        costo_base=costo,
                        id_usuario=usuario.id_usuario,
                        descripcion=descripcion if descripcion else None,
                        duracion_aproximada=duracion if duracion else None,
                    )

                    print(
                        f"Servicio '{servicio_encontrado.nombre}' creado con costo ${costo}."
                    )

                except ValueError as e:
                    print("Error:", e)
                    continue

            id_servicio = servicio_encontrado.id_servicio

            fecha = leer_texto("Fecha (YYYY-MM-DD HH:MM): ")
            motivo = leer_texto("Motivo: ")
            estado = leer_texto("Estado (pendiente/confirmada/cancelada): ")

            try:
                fecha_hora = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
                fecha_hora = fecha_hora.replace(tzinfo=timezone.utc)

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
                    fecha_hora = datetime.strptime(nueva_fecha, "%Y-%m-%d %H:%M")
                    fecha_hora = fecha_hora.replace(tzinfo=timezone.utc)
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
            print("\n-- Eliminar cita --")

            id_cita = leer_uuid("Id cita: ")
            if not id_cita:
                print("ID inválido")
                continue

            cita_obj = cita.obtener_por_id(id_cita)
            if not cita_obj:
                print("La cita no existe")
                continue

            if cita_obj.id_paciente != usuario.id_usuario:
                print("No puedes eliminar esta cita")
                continue

            confirmacion = leer_texto("¿Seguro que deseas eliminar la cita? (s/n): ")

            if confirmacion.lower() == "s":
                eliminado = cita.eliminar_cita(id_cita)

                if eliminado:
                    print("Cita eliminada correctamente")
                else:
                    print("No se pudo eliminar la cita")
            else:
                print("Operación cancelada")

        elif op == "5":
            print("\n-- Generar factura --")

            id_cita = leer_uuid("ID cita: ")
            if not id_cita:
                print("ID inválido")
                continue

            cita_obj = cita.obtener_por_id(id_cita)
            if not cita_obj:
                print("La cita no existe")
                continue

            paciente_obj = None
            for p in paciente.obtener_todos():
                if p.id_usuario == usuario.id_usuario:
                    paciente_obj = p
                    break

            if not paciente_obj:
                print("No tienes perfil de paciente")
                continue

            if cita_obj.id_paciente != paciente_obj.id_paciente:
                print("No puedes generar factura de esta cita")
                continue

            facturas = factura.obtener_todos()
            if any(f.id_cita == id_cita for f in facturas):
                print("Ya existe factura para esta cita")
                continue

            servicio_obj = servicio.obtener_por_id(cita_obj.id_servicio)

            if not servicio_obj:
                print("Servicio no encontrado")
                continue

            total = servicio_obj.costo_base

            estado_pago = leer_texto("Estado de pago (Pendiente/Pagado/Cancelado): ")
            metodo_pago = leer_texto(
                "Método de pago (Efectivo/Tarjeta/Transferencia): "
            )

            try:
                factura.crear_factura(
                    id_cita=id_cita,
                    total=total,
                    estado_pago=estado_pago,
                    fecha_pago=datetime.now(timezone.utc),
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
            try:
                nombre_medico = leer_texto("Nombre del médico: ")
                if not nombre_medico:
                    print("Nombre obligatorio")
                    continue

                id_usuario = leer_uuid("Id usuario: ")
                if not id_usuario:
                    print("ID de usuario inválido")
                    continue

                lista_especialidades = especialidad.obtener_todas()
                print("\n-- Especialidades disponibles --")
                for e in lista_especialidades:
                    print(f"{e.id_especialidad} | {e.nombre}")

                nombre_espe = leer_texto("Nombre de la especialidad: ")
                if not nombre_espe:
                    print("Especialidad obligatoria")
                    continue

                espe_encontrada = None
                for e in lista_especialidades:
                    if e.nombre.lower() == nombre_espe.lower():
                        espe_encontrada = e
                        break

                if not espe_encontrada:
                    descripcion = leer_texto(
                        "Descripción de la especialidad (opcional): "
                    )
                    espe_encontrada = especialidad.crear_especialidad(
                        nombre=nombre_espe,
                        id_usuario=id_usuario,
                        descripcion=descripcion if descripcion else None,
                    )
                    print(f"Especialidad '{espe_encontrada.nombre}' creada.")

                telefono_medico = leer_texto("Teléfono (opcional): ")

                medico.crear_medico(
                    nombre=nombre_medico,
                    id_usuario=id_usuario,
                    id_especialidad=espe_encontrada.id_especialidad,
                    telefono=telefono_medico if telefono_medico else None,
                )

                print("Médico creado exitosamente.")

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

            nombre_espe = leer_texto("Nueva especialidad: ")
            if not nombre_espe:
                print("Campo obligatorio")
                continue

            espe_encontrada = None
            for e in especialidad.obtener_todas():
                if e.nombre.lower() == nombre_espe.lower():
                    espe_encontrada = e
                    break

            if not espe_encontrada:
                try:
                    espe_encontrada = especialidad.crear_especialidad(
                        nombre=nombre_espe, id_usuario=usuario.id_usuario
                    )
                    print(f"Especialidad '{espe_encontrada.nombre}' creada.")
                except ValueError as e:
                    print("Error:", e)
                    continue

            try:
                actualizado = medico.actualizar_medico(
                    id_medico,
                    id_usuario=usuario.id_usuario,
                    id_especialidad=espe_encontrada.id_especialidad,
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

                print("Enfermero creado")

            except Exception as e:
                print(f"Error: {e}")

        elif op == "3":
            id_h = leer_uuid("ID historial: ")

            if not id_h:
                print("ID inválido")
                continue

            try:
                historial.actualizar_historial(
                    id_historial=id_h,
                    id_usuario_edicion=usuario.id_usuario,
                    observaciones_enfermeria=leer_texto("Observaciones: "),
                )
                print("Historial actualizado")

            except Exception as e:
                print(f"Error: {e}")


def main() -> None:
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print(
            "Escribe que opcion de usuario desear accede: 1. paciente 2. medico 3. enfermero  0. Salir"
        )

        op = leer_texto("Opción: ")

        if op == "0":
            print(f"Hasta luego {usuario.nombre_completo}.")
            break

        if usuario.rol == "paciente":
            menu_paciente(usuario)

        elif usuario.rol == "medico":
            menu_medico(usuario)

        elif usuario.rol == "enfermero":
            menu_enfermero(usuario)

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
