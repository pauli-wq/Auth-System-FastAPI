import os
from pathlib import Path

from dotenv import load_dotenv

# obtener la ruta raiz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / "env"

load_dotenv(ENV_FILE)  # cargar variables de entorno

URL_DATABASE: str = os.getenv("DATABASE_URL", "sqlite:///./auth_system.db")


# manejar configuraciones
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALGORITHM = os.getenv("ALGORITHM", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()
