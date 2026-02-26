from .persona import Persona


class Enfermero(Persona):

    def __init__(
        self, id_persona: int, nombre: str, especialidad: str, id_sede: int
    ) -> None:
        """
        Inicializa un objeto Enfermero.

        Args:
            id_persona (int): Identificador único heredado de Persona.
            nombre (str): Nombre completo heredado de Persona.
            especialidad (str): Área o especialidad en la que trabaja.
            id_sede (int): Identificador de la sede donde labora
        """
        super().__init__(id_persona, nombre)

        self._especialidad = especialidad
        self._id_sede = id_sede

    def tomar_signos_vitales(self) -> None:
        """
        Simula la acción de tomar los signos vitales de un paciente.
        """
        print(f"El enfermero {self._nombre} va a tomar los signos vitales.")

    def administrar_medicamento(self, medicamento: str, paciente: str) -> None:
        """
        Simula la administración de un medicamento a un paciente.

        Args:
            medicamento (str): Nombre del medicamento a administrar.
            paciente (str): Nombre del paciente que recibirá el medicamento.
        """
        print(
            f"El enfermero {self._nombre} va a administrar el medicamento: {medicamento} al paciente: {paciente}."
        )

    def mostrar_info(self) -> str:
        """
        Devuelve la información del enfermero.

        Returns:
            str: Nombre del enfermero y su especialidad.
        """
        return f"Enfermero: {self._nombre} | Especialidad: {self._especialidad}"
