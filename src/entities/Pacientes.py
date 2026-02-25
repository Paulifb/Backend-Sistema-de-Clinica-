class Paciente:
    """
    Representa un paciente dentro del sistema de la clínica.

    Almacena información básica del paciente que puede ser consultada
    por otras partes del sistema.
    """

    def __init__(
        self,
        id_paciente: int,
        nombre: str,
        edad: int,
        diagnostico: str,
        correo: str,
        telefono: str,
    ) -> None:
        """
        Inicializa un objeto Paciente.

        Args:
            id_paciente (int): Identificador único del paciente.
            nombre (str): Nombre completo del paciente.
            edad (int): Edad del paciente.
            diagnostico (str): Diagnóstico actual del paciente.
            correo (str): Correo electrónico del paciente.
            telefono (str): Número de teléfono del paciente.


        """
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")

        self._id_paciente = id_paciente
        self._nombre = nombre
        self._edad = edad
        self._diagnostico = diagnostico
        self._correo = correo
        self._telefono = telefono

    @property
    def id_paciente(self) -> int:
        """Retorna el identificador único del paciente."""
        return self._id_paciente

    @property
    def nombre(self) -> str:
        """Retorna el nombre del paciente."""
        return self._nombre

    @property
    def edad(self) -> int:
        """Retorna la edad del paciente."""
        return self._edad

    @property
    def diagnostico(self) -> str:
        """Retorna el diagnóstico actual del paciente."""
        return self._diagnostico

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del paciente."""
        return self._correo

    @property
    def telefono(self) -> str:
        """Retorna el número de teléfono del paciente."""
        return self._telefono

    def obtener_informacion(self) -> str:
        """
        Retorna una cadena con la información principal del paciente.
        """
        return (
            f"ID: {self._id_paciente} | "
            f"Nombre: {self._nombre} | "
            f"Edad: {self._edad} años | "
            f"Diagnóstico: {self._diagnostico} | "
            f"Correo: {self._correo} | "
            f"Teléfono: {self._telefono}"
        )
