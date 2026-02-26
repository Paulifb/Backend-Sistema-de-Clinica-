from src.entities.persona import Persona


class Paciente(Persona):
    """
    Representa un paciente dentro del sistema de la clínica.
    Hereda de la clase Persona.
    """

    def __init__(
        self,
        id_persona: int,
        nombre: str,
        edad: int,
        diagnostico: str,
        correo: str,
        telefono: str,
    ) -> None:
        """
        Inicializa un objeto Paciente.

        Args:
            id_persona (int): Identificador único heredado de Persona.
            nombre (str): Nombre completo del paciente.
            edad (int): Edad del paciente.
            diagnostico (str): Diagnóstico actual del paciente.
            correo (str): Correo electrónico del paciente.
            telefono (str): Número de teléfono del paciente.
        """

        super().__init__(id_persona, nombre)

        if edad < 0:
            raise ValueError("La edad no puede ser negativa")

        self._edad = edad
        self._diagnostico = diagnostico
        self._correo = correo
        self._telefono = telefono

    @property
    def edad(self) -> int:
        """Retorna la edad del paciente."""
        return self._edad

    @property
    def diagnostico(self) -> str:
        """Retorna el diagnóstico del paciente."""
        return self._diagnostico

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico."""
        return self._correo

    @property
    def telefono(self) -> str:
        """Retorna el número de teléfono."""
        return self._telefono

    def obtener_informacion(self) -> str:
        """
        Devuelve la información básica del paciente.
        """
        return (
            f"Paciente: {self.nombre} | "
            f"Edad: {self._edad} años | "
            f"Diagnóstico: {self._diagnostico} | "
            f"Correo: {self._correo} | "
            f"Teléfono: {self._telefono}"
        )
