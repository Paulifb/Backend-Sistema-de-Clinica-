#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo 1: Ejercicios Prácticos de POO en Python
Docente: Alejandro Salgar Marín
ITM 2025-2
"""

print("EJERCICIOS PRÁCTICOS - MÓDULO 1: POO EN PYTHON")
print("=" * 60)


print("\nEJERCICIO 1: CLASE ESTUDIANTE")
print("-" * 40)

class Estudiante:
    """ Representa a un estudiantte con sus datos"""
    def __init__(self, nombre: str, edad: int, carrera: str) -> None:
        
        """Inicializa un nuevo estudiante.

        Args:
            nombre (str): Nombre completo del estudiante.
            edad (int): Edad del estudiante.
            carrera (str): Carrera que cursa.
            """
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.promedio = 0.0
        self.materias_inscritas = []
    
    def presentarse(self) -> str:
        """
        Devuelve una presentación del estudiante.
        Returns:
                  str: TExto con la presentacion del estudiante.
                  """
        return f"Hola, soy {self.nombre}, tengo {self.edad} años y estudio {self.carrera}."
    
    def inscribir_materia(self, materia: str) -> str:

        """ Inscribe una materia al estudiante.
        Args:
        materia: Nombre de la materia.
        Returns:}
        str:  Mensaje indicando el resultado de la inscripción.   
        """
        if materia not in self.materias_inscritas:
            self.materias_inscritas.append(materia)
            return f"{self.nom|bre} se ha inscrito en {materia}"
        else:
            return f"{self.nombre} ya está inscrito en {materia}"
    
    def agregar_nota(self, materia: str, nota: float)-> str:
        """
        Registra una nota y actualiza el promedio general.

        Args:
            materia (str): Materia a la que pertenece la nota.
            nota (float): Valor de la nota (0.0 a 5.0).

        Returns:
            str: Confirmación de la nota o mensaje de error.
        """
        if materia in self.materias_inscritas and 0.0 <= nota <= 5.0:
            if self.promedio == 0.0:
                self.promedio = nota
            else:
                total_materias = len(self.materias_inscritas)
                suma_actual = self.promedio * (total_materias - 1)
                self.promedio = (suma_actual + nota) / total_materias
            return f"Nota {nota} agregada a {materia}. Nuevo promedio: {self.promedio:.2f}"
        else:
            return "Error: materia no inscrita o nota inválida"


estudiante1 = Estudiante("María González", 20, "Ingeniería de Sistemas")
print(estudiante1.presentarse())

print(estudiante1.inscribir_materia("Programación I"))
print(estudiante1.inscribir_materia("Matemáticas"))
print(estudiante1.agregar_nota("Programación I", 4.5))
print(estudiante1.agregar_nota("Matemáticas", 4.2))


print("\nEJERCICIO 2: CLASE RECTÁNGULO")
print("-" * 40)

class Rectangulo:
      """Representa un rectángulo con base y altura."""
    def __init__(self, base: float, altura: float)-> None:
        """
        Inicializa el rectángulo validando dimensiones positivas.

        Args:
            base (float): Medida de la base.
            altura (float): Medida de la altura.

         """
        if base > 0 and altura > 0:
            self.base = base
            self.altura = altura
        else:
            raise ValueError("La base y altura deben ser valores positivos")
    
    def calcular_area(self) -> float:
         """
        Calcula el área del rectángulo.

        Returns:
            float: Área calculada.
        """
        return self.base * self.altura
    
    def calcular_perimetro(self)-> float:
         """
        Calcula el perímetro del rectángulo.

        Returns:
            float: Perímetro calculado.
        """
        return 2 * (self.base + self.altura)
    
    def es_cuadrado(self) -> bool:
       """
        Indica si el rectángulo es un cuadrado.

        Returns:
            bool: True si es cuadrado.
        """
        return self.base == self.altura
    
    def mostrar_info(self) -> str:
          """
        Devuelve un resumen de las propiedades del rectángulo.

        Returns:
            str: Información formateada.
        """
        return f"""
INFORMACIÓN DEL RECTÁNGULO
   Base: {self.base} unidades
   Altura: {self.altura} unidades
   Área: {self.calcular_area():.2f} unidades²
   Perímetro: {self.calcular_perimetro():.2f} unidades
   ¿Es cuadrado?: {'Sí' if self.es_cuadrado() else 'No'}
        """


try:
    rect1 = Rectangulo(5, 3)
    rect2 = Rectangulo(4, 4)
    
    print("Rectángulo 1:")
    print(rect1.mostrar_info())
    
    print("\nRectángulo 2:")
    print(rect2.mostrar_info())
    
except ValueError as e:
    print(f"❌ Error: {e}")


print("\nEJERCICIO 3: CLASE CUENTA BANCARIA MEJORADA")
print("-" * 40)

class CuentaBancaria:
    """Simula una cuenta bancaria básica."""
    def __init__(self, titular: str, saldo_inicial: float, tipo_cuenta: str ="ahorros")->None :
        """
        Inicializa la cuenta bancaria.

        Args:
            titular (str): Nombre del dueño de la cuenta.
            saldo_inicial (float): Monto de apertura.
            tipo_cuenta (str): 'ahorros' o 'corriente'.
        """
        self.titular = titular
        self.__saldo = saldo_inicial
        self.tipo_cuenta = tipo_cuenta
        self.activa = True
    
    def depositar(self, cantidad: float) ->str:
        """
    Deposita una cantidad en la cuenta.

    Args:
        cantidad: La cantidad a depositar.

    Returns:
        str: Mensaje de éxito o error.
    """
        if not self.activa:
            return "La cuenta está inactiva"
        
        if cantidad > 0:
            self.__saldo += cantidad
            return f"Depósito exitoso de ${cantidad:,.2f}. Nuevo saldo: ${self.__saldo:,.2f}"
        else:
            return "La cantidad debe ser mayor a 0"
    
    def retirar(self, cantidad: float) ->str:
          """
        Retira dinero de la cuenta.

        Args:
            cantidad (float): Cantidad a retirar.

        Returns:
            str: Resultado de la operación.
        """
          
        if not self.activa:
            return "La cuenta está inactiva"
        
        if cantidad > 0 and cantidad <= self.__saldo:
            self.__saldo -= cantidad
            return f"Retiro exitoso de ${cantidad:,.2f}. Saldo restante: ${self.__saldo:,.2f}"
        else:
            return "Fondos insuficientes o cantidad inválida"
    
    def consultar_saldo(self) -> str:
          """
        Consulta el saldo actual.

        Returns:
            str: Saldo disponible.
        """
         if self.activa:
            return f"Saldo actual: ${self.__saldo:,.2f}"
        else:
            return "La cuenta está inactiva"
    
    def obtener_resumen(self) -> str:
         """
        Devuelve un resumen de la cuenta.

        Returns:
            str: Información de la cuenta.
        """
        return f"""
RESUMEN DE CUENTA BANCARIA
   Titular: {self.titular}
   Tipo de cuenta: {self.tipo_cuenta.title()}
   Estado: {'Activa' if self.activa else 'Inactiva'}
   Saldo actual: ${self.__saldo:,.2f}
        """


cuenta1 = CuentaBancaria("Alejandro Salgar", 5000, "corriente")
cuenta2 = CuentaBancaria("María López", 2000, "ahorros")

print(cuenta1.obtener_resumen())
print(cuenta2.obtener_resumen())

print(f"\n{cuenta1.depositar(1500)}")
print(f"{cuenta1.retirar(800)}")
print(f"{cuenta1.consultar_saldo()}")

print(f"\n{cuenta2.depositar(300)}")
print(f"{cuenta2.consultar_saldo()}")

print(f"\n¡Todos los ejercicios completados exitosamente!")
print("=" * 60)