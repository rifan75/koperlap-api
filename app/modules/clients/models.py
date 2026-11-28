from sqlalchemy import String, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

    
class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    client_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
            String(255),
            nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    roles = relationship(
        "ClientRole",
        back_populates="client",
        cascade="all, delete-orphan",
    )