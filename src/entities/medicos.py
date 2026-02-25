class Medico:
    """
    Representa un médico dentro del sistema de la clínica.
    """

    def __init__(
        self,
        id_medico: int,
        nombre: str,
        especialidad: str,
        licencia: str,
    ) -> None:
        """
        Inicializa un objeto Medico.

        Args:
            id_medico (int): Identificador único del médico.
            nombre (str): Nombre del médico.
            especialidad (str): Especialidad médica.
            licencia (str): Número de licencia profesional.
        """
        self._id_medico = id_medico
        self._nombre = nombre
        self._especialidad = especialidad
        self._licencia = licencia

    def dar_diagnostico(self, paciente: str, diagnostico: str) -> None:
        """
        Simula la asignación de un diagnóstico a un paciente.

        Args:
            paciente (str): Nombre del paciente.
            diagnostico (str): Diagnóstico asignado.
        """
        print(
            f"El médico {self._nombre} ha asignado el diagnóstico "
            f"'{diagnostico}' al paciente {paciente}."
        )

    def mostrar_info(self) -> str:
        """
        Devuelve la información básica del médico.

        Returns:
            str: Información del médico.
        """
        return (
            f"Médico: {self._nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Licencia: {self._licencia}"
        )
