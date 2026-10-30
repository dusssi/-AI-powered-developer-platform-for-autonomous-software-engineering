from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

_password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return _password_hash.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return _password_hash.verify(password, password_hash)

def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": str(user_id), "iat": now, "exp": now + timedelta(minutes=settings.access_token_minutes)},
        settings.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )

def decode_access_token(token: str) -> UUID:
    settings = get_settings()
    payload = jwt.decode(
        token, settings.jwt_secret.get_secret_value(), algorithms=["HS256"],
        options={"require": ["sub", "exp"]},
    )
    return UUID(payload["sub"])
