from src.entities.Pacientes import Paciente
from src.entities.cita import Cita
from src.entities.enfermeros import Enfermero
from src.entities.factura import Factura
from src.entities.medicos import Medico
from datetime import datetime


def menu():
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
    citas = []
    enfermeros = []
    pacientes = []
    while True:
        menu()
        opcion = input("Seleccion una opción: ")
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

        elif opcion == "3":
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
            print("Información de la cita\n")
            for cita in citas:
                print(cita.info_cita())

        elif opcion == "6":
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
            print("Asistencia de Enfermeria\n")

            if enfermeros and pacientes:
                medicamento = input("Ingrese el medicamento a administrar: ")

                enfermero = enfermeros[0]
                paciente = pacientes[0]

                enfermero.administrar_medicamento(medicamento, paciente.nombre)
            else:
                print("Debe registrar al menos un enfermero y un paciente.")

        elif opcion == "8":
            print("Informacion del profesional\n")

        elif opcion == "9":
            print("Recibir diagnostico del doctor\n")

        elif opcion == "10":
            print("Recibir informacion del paciente\n")

        elif opcion == "11":
            print("Tramitar factura\n")

        elif opcion == "12":
            print("Saliendo del programa.")
            break

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
