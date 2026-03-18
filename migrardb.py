"""
Script para inicializar la base de datos en Neon.
Crea todas las tablas del sistema de clínica.
"""

import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

# Importación de entidades para el registro de modelos
import src.entities.cita
import src.entities.enfermero
import src.entities.eps
import src.entities.factura
import src.entities.historial
import src.entities.medico
import src.entities.servicio
import src.entities.especialidad
import src.entities.paciente
import src.entities.usuario

from src.database.config import create_tables

# Carga de variables de entorno
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


def main():
    """Ejecuta la creación de tablas y maneja errores de conexión."""
    try:
        print("Intentando crear tablas en Neon...")
        create_tables()
        print("¡Éxito! Tablas creadas correctamente.")
    except OperationalError as e:
        if "password authentication failed" in str(e).lower():
            print("Error: Contraseña de Neon incorrecta. Revisa tu .env")
        else:
            print(f"Error de conexión: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
