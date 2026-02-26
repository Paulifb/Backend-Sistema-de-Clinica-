from src.entities.persona import Persona


class Medico(Persona):
    """
    Representa un médico dentro del sistema de la clínica.
    Hereda de la clase Persona.
    """

    def __init__(
        self,
        id_persona: int,
        nombre: str,
        especialidad: str,
        licencia: str,
    ) -> None:
        """
        Inicializa un objeto Medico.

        Args:
            id_persona (int): Identificador único heredado de Persona.
            nombre (str): Nombre completo heredado de Persona.
            especialidad (str): Especialidad médica del profesional.
            licencia (str): Número de licencia profesional.
        """
        # Se eliminaron self._id_medico y self._nombre por ser redundantes
        super().__init__(id_persona, nombre)

        self._especialidad = especialidad
        self._licencia = licencia

    @property
    def especialidad(self) -> str:
        """Retorna la especialidad del médico."""
        return self._especialidad

    @property
    def licencia(self) -> str:
        """Retorna la licencia del médico."""
        return self._licencia
