class Enfermero:

    def __init__(
        self, id_enfermero: int, nombre: str, especialidad: str, id_sede: int
    ) -> None:
        """
        Inicializa un objeto Enfermero.

        Args:
            id_enfermero (int): Identificador único del enfermero.
            nombre (str): Nombre del enfermero.
            especialidad (str): Área o especialidad en la que trabaja.
            id_sede (int): Identificador de la sede donde labora
        """
        self.id_enfermero = id_enfermero
        self.nombre = nombre
        self.especialidad = especialidad
        self.id_sede = id_sede

    def tomar_signos_vitales(self) -> None:
        print(f"El enfermero {self.nombre} va a tomar los signos vitales.")

    def administrar_medicamento(self, medicamento: str, paciente: str) -> None:
        print(
            f"El enfermero {self.nombre} va a administrar el medicamento: {medicamento} al paciente: {paciente}."
        )
