from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class MemberRole(Base):
    __tablename__ = "member_roles"

    __table_args__ = (
        UniqueConstraint(
            "member_id",
            "role_id",
            name="uq_member_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    member = relationship(
        "Member",
        back_populates="roles",
    )

    role = relationship(
        "Role",
    )


class ClientRole(Base):
    __tablename__ = "client_roles"

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "role_id",
            name="uq_client_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    client = relationship(
        "Client",
        back_populates="roles",
    )

    role = relationship(
        "Role",
    )

class AdminRole(Base):
    __tablename__ = "admin_roles"

    __table_args__ = (
        UniqueConstraint(
            "admin_id",
            "role_id",
            name="uq_admin_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    admin = relationship(
        "Admin",
        back_populates="roles",
    )

    role = relationship(
        "Role",
    )