class Persona:
    """
    Representa una persona dentro del sistema de la clínica.
    Contiene información básica común a pacientes y profesionales.
    """

    def __init__(self, id_persona: int, nombre: str) -> None:
        """
        Inicializa una persona.

        Args:
            id_persona (int): Identificador único.
            nombre (str): Nombre completo.
        """
        self._id_persona = id_persona
        self._nombre = nombre

    @property
    def id_persona(self) -> int:
        """Retorna el identificador único."""
        return self._id_persona

    @property
    def nombre(self) -> str:
        """Retorna el nombre de la persona."""
        return self._nombre
