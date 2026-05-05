from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.config import create_tables
from fastapi.middleware.cors import CORSMiddleware


from . import (
    cita,
    enfermero,
    historial,
    usuario,
    medico,
    especialidad,
    servicio,
    paciente,
    eps,
    factura,
    tratamiento,
)


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
    import src.entities.medico  # noqa: F401
    import src.entities.especialidad  # noqa: F401
    import src.entities.servicio  # noqa: F401
    import src.entities.paciente  # noqa: F401
    import src.entities.eps  # noqa: F401
    import src.entities.factura  # noqa: F401
    import src.entities.tratamiento  # noqa: F401

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(medico.router)
app.include_router(especialidad.router)
app.include_router(servicio.router)
app.include_router(usuario.router)
app.include_router(cita.router)
app.include_router(enfermero.router)
app.include_router(historial.router)
app.include_router(paciente.router)
app.include_router(eps.router)
app.include_router(factura.router)
app.include_router(tratamiento.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """
    Endpoint de verificación del estado de la API.

    Permite comprobar rápidamente si la API está funcionando correctamente.

    Returns:
        Un diccionario con el estado de la aplicación.
    """
    return {"status": "ok"}
