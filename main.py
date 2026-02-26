"""
Módulo principal del Sistema de Gestión de Citas Médicas.
Este módulo contiene la lógica del menú y la integración de las entidades del sistema.
"""

from src.entities.Pacientes import Paciente
from src.entities.cita import Cita
from src.entities.enfermeros import Enfermero
from src.entities.factura import Factura
from src.entities.medicos import Medico


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
            print("Registrar enfermero\n")

        elif opcion == "4":
            print("Agendar cita\n")

        elif opcion == "5":
            print("Información de la cita\n")

        elif opcion == "6":
            print("Re programar cita\n")

        elif opcion == "7":
            print("Asistencia de Enfermeria\n")

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

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
