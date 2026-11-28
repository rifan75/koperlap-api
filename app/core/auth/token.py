
import uuid
import secrets
import hashlib

from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.core.principal import Principal
from app.config import settings

from app.core.auth.models import AuthSession, RefreshToken

from app.core.auth.models import AuthSession,RefreshToken

from app.core.principal import load_principal
from app.core.rbac.service import get_user_authorities


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

def generate_refresh_token() -> tuple[str, str]:

    token = secrets.token_urlsafe(48)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    return token, token_hash


async def issue_token_pair(
    db: AsyncSession,
    principal: Principal,
    roles: list[str],
    permissions: list[str],
):

    now = datetime.now(timezone.utc)

    session_expire = now + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    # 1. Create authenticated session
    session = AuthSession(
        principal_id=principal.id,
        principal_type=principal.type,
        expires_at=session_expire,
    )

    db.add(session)

    await db.flush()

    # 2. Generate opaque refresh token
    raw_refresh_token, refresh_token_hash = (
        generate_refresh_token()
    )

    family_id = uuid.uuid4()

    refresh = RefreshToken(
        session_id=session.id,
        family_id=family_id,
        token_hash=refresh_token_hash,
        expires_at=session_expire,
    )

    db.add(refresh)

    # 3. Create access JWT
    subject = f"{principal.type}:{principal.id}"

    access_token = create_access_token(
        subject=subject,
        claims={
            "principal_id": principal.id,
            "principal_type": principal.type,
            "session_id": str(session.id),
            "roles": roles,
            "permissions": permissions,
        },
    )

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "expires_in": (
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        "session_id": str(session.id),
    }

async def rotate_refresh_token(
    db: AsyncSession,
    raw_token: str,
):
    now = datetime.now(timezone.utc)

    token_hash = hash_refresh_token(raw_token)

    # 1. Lock refresh token to prevent concurrent rotation
    result = await db.execute(
        select(RefreshToken)
        .where(
            RefreshToken.token_hash == token_hash
        )
        .with_for_update()
    )

    old_token = result.scalar_one_or_none()

    if old_token is None:
        return None

    # 2. Detect reuse of an already-consumed token
    if old_token.consumed_at is not None:

        await db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.family_id == old_token.family_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        await db.execute(
            update(AuthSession)
            .where(
                AuthSession.id == old_token.session_id,
                AuthSession.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        return {
            "reuse_detected": True,
        }

    # 3. Validate refresh token
    if (
        old_token.revoked_at is not None
        or old_token.expires_at <= now
    ):
        return None

    # 4. Lock and validate session
    session_result = await db.execute(
        select(AuthSession)
        .where(
            AuthSession.id == old_token.session_id
        )
        .with_for_update()
    )

    session = session_result.scalar_one_or_none()

    if (
        session is None
        or session.revoked_at is not None
        or session.expires_at <= now
    ):
        return None

    # 5. Reconstruct principal
    principal = Principal(
        id=session.principal_id,
        type=session.principal_type,
    )

    # 6. Validate account
    identity = await load_principal(
        db,
        principal,
    )

    if not identity:
        session.revoked_at = now

        await db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.session_id == session.id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )

        return None

    # 7. Resolve current RBAC
    roles, permissions = await get_user_authorities(
        db,
        principal,
    )

    # 8. Generate new refresh token
    new_raw_token, new_token_hash = generate_refresh_token()

    new_token = RefreshToken(
        session_id=session.id,
        family_id=old_token.family_id,
        token_hash=new_token_hash,
        expires_at=old_token.expires_at,
    )

    db.add(new_token)

    await db.flush()

    # 9. Consume old token
    old_token.consumed_at = now
    old_token.replaced_by = new_token.id

    # 10. Generate new access token
    subject = f"{principal.type}:{principal.id}"

    access_token = create_access_token(
        subject=subject,
        claims={
            "principal_id": principal.id,
            "principal_type": principal.type,
            "session_id": str(session.id),
            "roles": roles,
            "permissions": permissions,
        },
    )

    return {
        "access_token": access_token,
        "refresh_token": new_raw_token,
        "expires_in": (
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        "user": {
            "id": str(principal.id),
            "type": principal.type,
            "roles": roles,
            "permissions": permissions,
        },
    }
