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
        Inicializa un objeto Medico utilizando la base de Persona.
        """
        super().__init__(id_persona, nombre)
        self._especialidad = especialidad
        self._licencia = licencia

    def dar_diagnostico(self, paciente: str, diagnostico: str) -> None:
        """
        Lógica de impresión para la opción 7 del menú.
        """
        print(f"\n{'='*30}")
        print(f"SISTEMA DE DIAGNÓSTICO")
        print(f"Médico: {self.nombre}")
        print(f"Paciente: {paciente}")
        print(f"Resultado: {diagnostico}")
        print(f"{'='*30}\n")

    @property
    def especialidad(self) -> str:
        """Retorna la especialidad del médico."""
        return self._especialidad

    @property
    def licencia(self) -> str:
        """Retorna la licencia del médico."""
        return self._licencia

    def __str__(self) -> str:
        """
        Facilita la visualización en la opción 6 del menú.
        Permite usar print(objeto_medico) directamente.
        """
        return f"Profesional: {self.nombre} | Especialidad: {self.especialidad} | Licencia: {self.licencia}"
