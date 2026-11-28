from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    member_assignments = relationship(
        "MemberRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    admin_assignments = relationship(
        "AdminRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    client_assignments = relationship(
        "ClientRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    permissions = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )