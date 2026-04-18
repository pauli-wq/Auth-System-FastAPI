from datetime import datetime

from pydantic import BaseModel, EmailStr


# Base
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None


# Crear usuario
class UserCreate(UserBase):
    password: str


# Actualizar usuario
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None


# El response que debe devolver la API
class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class ConfigDict:
        from_attributes = True


# Usuario en DB (con hashed_password)
class UserInDB(User):
    hashed_password: str
