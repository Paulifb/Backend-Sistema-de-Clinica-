from src.entities.Pacientes import Paciente
from src.entities.cita import Cita
from src.entities.enfermeros import Enfermero
from src.entities.factura import Factura
from src.entities.medicos import Medico


def menu():
    print("Sistema de Gestión de Citas Médicas/n")
    print("1. Registrar paciente")
    print("2. Registrar cita")
    print("3. Información de la cita")
    print("4. Re programar cita")
    print("5. Asistencia de Enfermeria")
    print("6. Informacion del profesional")
    print("7. Recibir diagnostico del doctor")
    print("8. Recibir informacion del paciente")
    print("9. Tramitar factura")
    print("10. Salir")


def main() -> None:
    cita = {}
    while True:
        menu()
        opcion = input("Seleccion una opción: ")
        if opcion not in ["1", "2", "3"]:
            print("Opción no válida. Por favor, intente de nuevo.")
            continue

        if opcion == "1":
            print("You selected Option 1")

        elif opcion == "2":
            print("You selected Option 2")

        elif opcion == "3":
            print("Exiting the program.")

        elif opcion == "4":
            print("You selected Option 4")

        elif opcion == "5":
            print("You selected Option 5")

        elif opcion == "6":
            print("You selected Option 6")

        elif opcion == "7":
            print("You selected Option 7")

        elif opcion == "8":
            print("You selected Option 8")

        elif opcion == "9":
            print("You selected Option 9")

        elif opcion == "10":
            print("Saliendo del programa.")
            break

        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()
