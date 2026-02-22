class Paciente:
    def __init__(self, id_paciente: int, nombre: str, edad: int, diagnostico: str):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.edad = edad
        self.diagnostico = diagnostico

    def imprimir_data(self):
        print(
            f"Id: {self.id_paciente}, nombre: {self.nombre}, edad: {self.edad} años, diagnóstico: {self.diagnostico}"
        )


paciente1 = Paciente(101, "Ana Torres", 28, "Gripe")
paciente1.imprimir_data()
