class Enfermero:
    def __init__(self, id_enfermero: int, nombre: str, especialidad: str, id_sede: int):
        self.id_enfermero = id_enfermero
        self.nombre = nombre
        self.especialidad = especialidad
        self.id_sede = id_sede

    def imprimir_data(self):
        print(
            f"Id: {self.id_enfermero}, nombre: {self.nombre}, especialidad: {self.especialidad} y el id de la sede: {self.id_sede}"
        )


enfermero1 = Enfermero(23434, "Sirio", "Pediatria", 345345)
enfermero1.imprimir_data()
