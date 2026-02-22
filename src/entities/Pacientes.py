class Paciente:
    """
    Representa un paciente dentro del sistema de clínica.
    Permite almacenar información básica del paciente.
    """

    def __init__(
        self, id_paciente: int, nombre: str, edad: int, diagnostico: str
    ) -> None:
        """
        Inicializa un objeto Paciente.

        Args:
            id_paciente (int): Identificador único del paciente.
            nombre (str): Nombre completo del paciente.
            edad (int): Edad del paciente.
            diagnostico (str): Diagnóstico actual del paciente.
        """

    self._id_paciente = id_paciente
    self._nombre = nombre
    self._edad = edad
    self._diagnostico = diagnostico


def obtener_informacion(self) -> str:
    return (
        f"Id: {self._id_paciente}, Nombre: {self._nombre}, "
        f"Edad: {self._edad} años, Diagnóstico: {self._diagnostico}"
    )


def actualizar_diagnostico(self, nuevo_diagnostico: str) -> None:
    """
    Actualiza el diagnóstico del paciente.
    """
    self._diagnostico = nuevo_diagnostico
