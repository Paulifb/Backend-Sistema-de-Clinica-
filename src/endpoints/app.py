from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.config import create_tables
from . import especialidad, medico, servicio


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Registra modelos y crea tablas si no existen
    import src.entities.especialidad  # noqa: F401
    import src.entities.medico  # noqa: F401
    import src.entities.servicio  # noqa: F401

    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(medico.router)
app.include_router(especialidad.router)
app.include_router(servicio.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
