from datetime import datetime, timezone, timedelta

from pwdlib import PasswordHash
import jwt

from src.core.settings import app_settings

password_hasher = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(password=plain_password)


def validate_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(
        password=plain_password,
        hash=hashed_password,
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        app_settings.secret_key,
        algorithm="HS256",
    )
    return encoded_jwt
