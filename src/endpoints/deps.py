from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.config import get_db

"""
DbSession es un alias de tipo que representa una sesión de base de datos
de SQLAlchemy gestionada automáticamente por FastAPI.

Utiliza Annotated para combinar:
- Session: el tipo de dato esperado (sesión de base de datos)
- Depends(get_db): la función que provee dicha sesión

Esto permite reutilizar fácilmente la dependencia en los endpoints,
evitando repetir código como:
    db: Session = Depends(get_db)

Ejemplo de uso:
    def endpoint(db: DbSession):
        ...
"""
DbSession = Annotated[Session, Depends(get_db)]
