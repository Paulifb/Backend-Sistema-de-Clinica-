"""
Arranca la API FastAPI (uvicorn).

  python run_api.py
Arranca la API FastAPI (uvicorn).rando e

  python main.py

Documentación interactiva: http://127.0.0.1:8000/docs

Para crear tablas en la base de datos, usa: python migrardb.py
"""

import uvicorn

from src.endpoints.app import app

if __name__ == "__main__":
    # reload exige el string de importación; `app` sigue disponible para tests / ASGI
    uvicorn.run(
        "src.endpoints.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
