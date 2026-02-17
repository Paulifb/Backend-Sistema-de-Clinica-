class Medico:
    def __init__(self, id_medico: int, nombre: str, especialidad: str, licencia: str):
        self.id_medico = id_medico
        self.nombre = nombre
        self.especialidad = especialidad
        self.licencia = licencia

    def imprimir_data(self):
        print(
            f"Médico ID: {self.id_medico}, Nombre: {self.nombre}, "
            f"Especialidad: {self.especialidad} y su N° de Licencia: {self.licencia}"
        )


# Ejemplo de uso
medico1 = Medico(1020, "Dra. Elena Rossi", "Cardiología", "LIC-8899")
medico1.imprimir_data()
