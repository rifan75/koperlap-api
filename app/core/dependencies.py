
from datetime import datetime, timezone
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db

from app.core.security import decode_access_token
from app.core.principal import Principal

from app.core.auth.models import AuthSession


# =========================
# BEARER AUTHENTICATION
# =========================

bearer_scheme = HTTPBearer(
    auto_error=False,
)


async def get_current_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: AsyncSession = Depends(get_db),
):

    # 1. Check Authorization header
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Verify JWT
    payload = decode_access_token(
        credentials.credentials
    )

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Extract session ID
    try:
        session_id = UUID(payload["session_id"])

        principal_id = int(payload["principal_id"])
        principal_type = payload["principal_type"]

        # Validate subject consistency
        expected_subject = (
            f"{principal_type}:{principal_id}"
        )

        if payload["sub"] != expected_subject:
            raise ValueError("Invalid subject")

    except (KeyError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token claims",
        )

    # 4. Validate authenticated session
    result = await db.execute(
        select(AuthSession).where(
            AuthSession.id == session_id,
            AuthSession.principal_id == principal_id,
            AuthSession.principal_type == principal_type,
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > datetime.now(timezone.utc),
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Session expired or revoked",
        )

    return payload


# =========================
# CURRENT PRINCIPAL
# =========================

async def get_current_principal(
    payload: dict = Depends(get_current_token),
) -> Principal:

    return Principal(
        id=payload["principal_id"],
        type=payload["principal_type"],
    )


# =========================
# RBAC PERMISSION CHECK
# =========================

def require_permission(permission: str):

    async def permission_checker(
        payload: dict = Depends(get_current_token),
    ):

        permissions = payload.get("permissions", [])

        if permission not in permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return payload

    return permission_checker
