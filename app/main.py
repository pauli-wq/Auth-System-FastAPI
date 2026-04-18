from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import Base, engine
from app.routes import auth, users


# al iniciar la API se ejecuta este context manager para crear las tablas
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        print("SHUTDOWN")
        engine.dispose()


app = FastAPI(
    title="Auth System",
    description="A Simple Authentication System Using FastAPI.",
    lifespan=lifespan,
)

# routers de los endpoints
app.include_router(auth.router)
app.include_router(users.router)

# middleware para CORS
# permite solicitudes desde los orígenes especificados en las configuraciones
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS_ALLOWED,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Auth System API!"}
