from .paciente import Paciente
from .medicos import Medico
from .enfermeros import Enfermero
from datetime import datetime


class Cita:
    """
    Representa una cita médica dentro del sistema de la clínica.

    Una cita relaciona a un paciente con un profesional de la salud
    (médico o enfermero) en una fecha y hora determinada.
    """

    def __init__(
        self,
        id_cita: int,
        fecha_hora: datetime,
        paciente: Paciente,
        profesional: Medico | Enfermero,
    ) -> None:
        """
        Inicializa una nueva cita médica.

        Args:
            id_cita (int): Identificador único de la cita.
            fecha_hora (datetime): Fecha y hora programada para la cita.
            paciente (Paciente): Paciente que asistirá a la cita.
            profesional (Medico | Enfermero): Profesional que atenderá la cita.

        Raises:
            ValueError: Si el paciente es None.
        """

        if paciente is None:
            raise ValueError("El paciente no puede ser None.")

        self._id_cita = id_cita
        self._fecha_hora = fecha_hora
        self._paciente = paciente
        self._profesional = profesional

    @property
    def id_cita(self) -> int:
        """Retorna el identificador único de la cita."""
        return self._id_cita

    @property
    def fecha_hora(self) -> datetime:
        """Retorna la fecha y hora programada de la cita."""
        return self._fecha_hora

    def info_cita(self) -> str:
        """
        Devuelve la información principal de la cita en formato de texto.

        Returns:
            str: Cadena con el ID de la cita, fecha, paciente y profesional asignado.
        """
        return (
            f"Cita ID: {self._id_cita}\n"
            f"Fecha y Hora : {self._fecha_hora.strftime('%Y-%m-%d %H:%M')}\n"
            f"Paciente: {self._paciente.nombre}\n"
            f"Profesional: {self._profesional.nombre} ({type(self._profesional).__name__})"
        )

    def re_programar_cita(self, nueva_fecha_hora: datetime) -> None:
        """
        Modifica la fecha y hora de una cita existente.

        Args:
            nueva_fecha_hora (datetime): Nueva fecha y hora para la cita.
        """
        self._fecha_hora = nueva_fecha_hora
