
from datetime import datetime, timedelta, timezone
import uuid
import bcrypt
from jose import JWTError, jwt

from app.config import settings

ALGORITHM = settings.JWT_ALGORITHM
PRIVATE_KEY = settings.JWT_PRIVATE_KEY_PATH.read_text()
PUBLIC_KEY = settings.JWT_PUBLIC_KEY_PATH.read_text()


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except (ValueError, TypeError):
        return False


def create_access_token(
    subject: str,
    claims: dict,
) -> str:

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        **claims,
        "sub": subject,
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "iat": now,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM,
    )

def decode_access_token(token: str) -> dict:

    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        if payload.get("type") != "access":
            return {}

        return payload

    except JWTError:
        return {}
