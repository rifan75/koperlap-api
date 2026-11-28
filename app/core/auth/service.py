from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.modules.admins.models import Admin

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    state: str = Field(min_length=32, max_length=256)

    code_challenge: str = Field(
        min_length=43,
        max_length=128,
    )

    code_challenge_method: str = "S256"

class AuthorizeRequest(BaseModel):
    code: str
    code_verifier: str

async def authenticate_admin(db: AsyncSession, email: str, password: str) -> Admin | None:
    result = await db.execute(
        select(Admin).where(
            Admin.email == email.lower(),
            Admin.is_active == True,
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        return None
    return user





