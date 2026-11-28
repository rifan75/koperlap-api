from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.models import AuthSession, RefreshToken


async def revoke_session(
    db: AsyncSession,
    session_id: UUID,
):
    now = datetime.now(timezone.utc)

    # Revoke session
    await db.execute(
        update(AuthSession)
        .where(
            AuthSession.id == session_id,
            AuthSession.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )

    # Revoke all refresh tokens belonging to session
    await db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.session_id == session_id,
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )