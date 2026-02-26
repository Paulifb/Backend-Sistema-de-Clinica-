"""
Módulo principal del Sistema de Gestión de Citas Médicas.
Este módulo contiene la lógica del menú y la integración de las entidades del sistema.
"""

from src.entities.Pacientes import Paciente
from src.entities.cita import Cita
from src.entities.enfermeros import Enfermero
from src.entities.factura import Factura
from src.entities.medicos import Medico
from datetime import datetime


def menu():
    """Imprime las opciones disponibles en el sistema."""
    print("Sistema de Gestión de Citas Médicas\n")
    print("1. Registrar paciente")
    print("2. Registrar médico")
    print("3. Registrar enfermero")
    print("4. Registrar cita")
    print("5. Información de la cita")
    print("6. Re programar cita")
    print("7. Asistencia de Enfermeria")
    print("8. Informacion del profesional")
    print("9. Recibir diagnostico del doctor")
    print("10. Recibir informacion del paciente")
    print("11. Tramitar factura")
    print("12. Salir")


def main() -> None:
    """
    Ejecuta el ciclo principal del menú y gestiona la persistencia temporal
    de los objetos registrados durante la sesión.
    """
    citas = []
    medicos = []
    enfermeros = []
    facturas = []
    pacientes = []
    while True:
        menu()
        opcion = input("Seleccion una opción: ")
        if opcion not in ["1", "2", "3"]:

            if opcion not in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
            ]:
                print("Opción no válida. Por favor, intente de nuevo.")
                continue

        if opcion == "1":
            print("Registrar paciente\n")

        elif opcion == "2":
            print("Registrar médico\n")
            """Captura datos, instancia la clase Medico y almacena el objeto en la lista."""
            print("Registrar médico\n")
            id_medico = int(input("Ingrese el ID del médico: "))
            nombre_medico = input("Ingrese el nombre del médico: ")
            especialidad = input("Ingrese la especialidad del médico: ")
            licencia = input("Ingrese la licencia del médico: ")

            nuevo_medico = Medico(id_medico, nombre_medico, especialidad, licencia)
            medicos.append(nuevo_medico)

            if nuevo_medico is not None:
                print("Médico registrado exitosamente.")

        elif opcion == "3":
            """
            Permite registrar un nuevo enfermero en el sistema.

            Solicita al usuario los datos básicos del enfermero:
            - ID del enfermero.
            - Nombre completo.
            - Especialidad.
            - ID de la sede donde trabaja.

            Luego, crea un objeto de tipo Enfermero con la información ingresada
            y lo agrega a la lista de enfermeros del sistema.

            Finalmente, muestra un mensaje de confirmación indicando que el
            registro fue realizado exitosamente.
            """

            print("Registrar enfermero\n")
            id_enfermero = int(input("Ingrese el ID del enfermero: "))
            nombre_enfermero = input("Ingrese el nombre del enfermero: ")
            especialidad_enfermero = input("Ingrese la especialidad del enfermero: ")
            id_sede_enfermero = int(
                input("Ingrese el ID de la sede donde labora el enferomero: ")
            )
            enfermero = Enfermero(
                id_enfermero,
                nombre_enfermero,
                especialidad_enfermero,
                id_sede_enfermero,
            )
            enfermeros.append(enfermero)

            if enfermeros is not None:
                print("Enfermero registrado exitosamente.")

        elif opcion == "4":

            """
            Permite agendar una nueva cita médica en el sistema.

            Solicita al usuario:
            - El código único de la cita.
            - La fecha y hora de la cita en formato YYYY-MM-DD HH:MM.

            Valida que existan pacientes registrados; en caso contrario,
            solicita registrar uno antes de continuar. También verifica
            que haya al menos un profesional de la salud (médico o enfermero).

            Selecciona automáticamente el último paciente registrado y el
            último profesional disponible (priorizando médicos y, si no hay,
            enfermeros). Luego crea un objeto de tipo Cita con la información
            ingresada, lo agrega a la lista de citas y confirma el agendamiento.
            """
            print("Agendar cita\n")
            codigo_cita = int(input("Ingrese el código de la cita: "))
            fecha_str = input("Ingrese la fecha y hora (YYYY-MM-DD HH:MM): ")
            fecha_hora = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

            if not pacientes:
                print(
                    "No hay pacientes registrados. Por favor, registre un paciente primero."
                )
                continue

            if not enfermeros and not medicos:
                print(
                    "No hay profesionales registrados. Por favor, registre un médico o enfermero primero."
                )
                continue

            paciente = pacientes[-1]
            if medicos:
                profesional = medicos[-1]
            else:
                profesional = enfermeros[-1]

            cita = Cita(codigo_cita, fecha_hora, paciente, profesional)

            citas.append(cita)
            print("Cita agendada exitosamente.")

        elif opcion == "5":
            """
            Muestra la información de todas las citas registradas en el sistema.

            Recorre la lista de citas existentes y presenta los detalles de cada
            una utilizando el método info_cita(), el cual devuelve los datos
            relevantes de la cita como paciente, profesional, fecha y hora.

            Permite al usuario visualizar de manera clara las citas agendadas.
            """
            print("Información de la cita\n")
            for cita in citas:
                print(cita.info_cita())

        elif opcion == "6":
            """
            Permite reprogramar una cita médica existente.

            Solicita al usuario el código de la cita que desea modificar
            y la nueva fecha y hora en formato YYYY-MM-DD HH:MM.

            Busca la cita dentro de la lista de citas registradas. Si la encuentra,
            actualiza la fecha utilizando el método re_programar_cita() y muestra
            un mensaje de confirmación. Si no se encuentra, informa al usuario
            que la cita no existe en el sistema.
            """
            print("Re programar cita\n")
            buscar_cita = input("Ingrese el código de la cita a re programar: ")
            nueva_fecha_str = input("Nueva fecha: ")
            nueva_fecha = datetime.strptime(nueva_fecha_str, "%Y-%m-%d %H:%M")

            cita_encontrada = False
            for cita in citas:
                if cita.id_cita == int(buscar_cita):
                    cita.re_programar_cita(nueva_fecha)
                    print("Cita re programada exitosamente.")
                    cita_encontrada = True
                    break

            if not cita_encontrada:
                print("Cita no encontrada. Por favor, intente de nuevo.")

        elif opcion == "7":
            """
            Permite registrar una asistencia de enfermería en el sistema.

            Verifica que exista al menos un enfermero y un paciente registrados.
            Si se cumplen estas condiciones, solicita al usuario el nombre del
            medicamento a administrar.

            Selecciona el primer enfermero y el primer paciente de las listas
            registradas, y utiliza el método administrar_medicamento() para
            registrar la administración del medicamento.

            En caso de no haber enfermeros o pacientes, muestra un mensaje
            indicando que deben ser registrados previamente.
            """
            print("Asistencia de Enfermeria\n")

            if enfermeros and pacientes:
                medicamento = input("Ingrese el medicamento a administrar: ")

                enfermero = enfermeros[0]
                paciente = pacientes[0]

                enfermero.administrar_medicamento(medicamento, paciente.nombre)
            else:
                print("Debe registrar al menos un enfermero y un paciente.")

        elif opcion == "8":
            """Muestra la información del médico utilizando el método __str__ definido en su clase."""
            print("Informacion del profesional\n")
            if medicos:
                for m in medicos:
                    print(m)

        elif opcion == "9":
            """Captura datos del paciente y utiliza un objeto médico para emitir un diagnóstico."""
            print("Recibir diagnostico del doctor\n")
            if medicos:
                paciente = input("Nombre del paciente: ")
                diagnostico = input("Diagnóstico: ")
                medicos[0].dar_diagnostico(paciente, diagnostico)

        elif opcion == "10":
            print("Recibir informacion del paciente\n")

        elif opcion == "11":
            print("Tramitar factura\n")

        elif opcion == "12":
            print("Saliendo del programa.")
            break


if __name__ == "__main__":
    main()
