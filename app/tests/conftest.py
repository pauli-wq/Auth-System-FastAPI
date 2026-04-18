import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_pass_hash
from app.database.database import Base, get_db
from app.main import app
from app.models.user import User

# Creamos una base de datos temporal para las pruebas (SQLite en memoria)
DATABASE_URL_TEST = "sqlite:///:memory:"
test_engine = create_engine(
    DATABASE_URL_TEST, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# usuario para test
@pytest.fixture
def test_user(db_session: Session):
    user = User(
        username="testuser",
        full_name="Andres Perez",
        email="test@example.com",
        is_active=True,
        hashed_password=get_pass_hash("secret123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# Creamos las tablas en la base de datos de prueba
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# Proporcionamos una sesión de base de datos para las pruebas y rollback después de cada prueba
@pytest.fixture(scope="function")
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    transaction.rollback()  # deshacemos los cambios después de cada prueba
    session.close()
    connection.close()


# Sobrescribimos la dependencia get_db para usar la sesión de prueba
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    # solo eliminamos la override que añadimos
    app.dependency_overrides.pop(get_db, None)
