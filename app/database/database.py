from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import URL_DATABASE

# Crear engine
engine = create_engine(
    URL_DATABASE,
    connect_args={"check_same_thread": False} if "sqlite" in URL_DATABASE else {},
)

# Crear sesiones de DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependencia para obtener BD session en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()
