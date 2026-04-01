from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables

from . import cita, enfermero, historial, usuario


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación FastAPI.

    Este contexto se ejecuta al iniciar la aplicación y permite
    realizar configuraciones iniciales, como el registro de modelos
    y la creación automática de tablas en la base de datos.

    Args:
        _app: Instancia de la aplicación FastAPI.

    Yields:
        Control al ciclo de vida de la aplicación.
    """

    # Registra modelos y crea tablas si no existen (misma lógica que init_db.py)
    import src.entities.cita  # noqa: F401
    import src.entities.enfermero  # noqa: F401
    import src.entities.historial  # noqa: F401
    import src.entities.usuario  # noqa: F401

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(usuario.router)
app.include_router(cita.router)
app.include_router(enfermero.router)
app.include_router(historial.router)


@app.get("/health")
def health() -> dict[str, str]:
    """
    Endpoint de verificación del estado de la API.

    Permite comprobar rápidamente si la API está funcionando correctamente.

    Returns:
        Un diccionario con el estado de la aplicación.
    """
    return {"status": "ok"}
