from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings

pass_hash = PasswordHash([Argon2Hasher()])


# Verifica si la clave coincide con el hash
def verify_pass(plain_pass: str, hashed_pass: str) -> bool:
    return pass_hash.verify(plain_pass, hashed_pass)


# Genera un hash
def get_pass_hash(password: str):
    return pass_hash.hash(password)


# Creamos un token JWT de acceso
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
