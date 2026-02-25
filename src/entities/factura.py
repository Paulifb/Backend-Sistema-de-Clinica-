class Factura:
    """
    Representa una factura generada por los servicios médicos
    prestados en la clínica.

    Permite registrar la información de cobro asociada a una cita
    y gestionar el estado de pago.
    """

    def __init__(self, id_factura: int, paciente, cita, valor: float) -> None:
        """
        Inicializa una factura.

        Args:
            id_factura (int): Identificador único de la factura.
            paciente: Objeto Paciente asociado a la factura.
            cita: Objeto Cita relacionado con el servicio prestado.
            valor (float): Valor total a pagar.
        """

        if valor < 0:
            raise ValueError("El valor de la factura no puede ser negativo.")

        self._id_factura = id_factura
        self._paciente = paciente
        self._cita = cita
        self._valor = valor
        self._estado = "Pendiente"

    def obtener_id(self) -> int:
        """
        Retorna el identificador de la factura.
        """
        return self._id_factura

    def obtener_valor(self) -> float:
        """
        Retorna el valor total de la factura.
        """
        return self._valor

    def obtener_estado(self) -> str:
        """
        Retorna el estado actual de la factura.
        """
        return self._estado

    def obtener_paciente(self):
        """
        Retorna el paciente asociado a la factura.
        """
        return self._paciente

    def obtener_cita(self):
        """
        Retorna la cita asociada a la factura.
        """
        return self._cita

    def obtener_informacion(self) -> str:
        """
        Retorna un resumen con la información de la factura.
        """
        return (
            f"Factura ID: {self._id_factura}\n"
            f"Paciente: {self._paciente._nombre}\n"
            f"Valor: ${self._valor}\n"
            f"Estado: {self._estado}"
        )

    def marcar_como_pagada(self) -> None:
        """
        Cambia el estado de la factura a 'Pagada'.
        """
        self._estado = "Pagada"

    def marcar_como_pendiente(self) -> None:
        """
        Cambia el estado de la factura a 'Pendiente'.
        """
        self._estado = "Pendiente"

    def actualizar_valor(self, nuevo_valor: float) -> None:
        """
        Actualiza el valor de la factura.

        Args:
            nuevo_valor (float): Nuevo valor de la factura.
        """
        if nuevo_valor < 0:
            raise ValueError("El valor no puede ser negativo.")

        self._valor = nuevo_valor
