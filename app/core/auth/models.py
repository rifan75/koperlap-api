
import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    BigInteger,
    CheckConstraint,
    Index,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    __table_args__ = (
        CheckConstraint(
            "principal_type IN ('member', 'client', 'admin')",
            name="ck_auth_sessions_principal_type",
        ),
        Index(
            "ix_auth_sessions_principal",
            "principal_type",
            "principal_id",
        ),
        Index(
            "ix_auth_sessions_expires_at",
            "expires_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    principal_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    principal_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    __table_args__ = (
        Index(
            "ix_refresh_tokens_token_hash",
            "token_hash",
            unique=True,
        ),
        Index(
            "ix_refresh_tokens_family_id",
            "family_id",
        ),
        Index(
            "ix_refresh_tokens_session_id",
            "session_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "auth_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    family_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    replaced_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "refresh_tokens.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    consumed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
