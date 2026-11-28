from pydantic import BaseModel
from typing import Literal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.members.models import Member
from app.modules.clients.models import Client
from app.modules.admins.models import Admin

PRINCIPAL_MODELS = {
    "member": Member,
    "client": Client,
    "admin": Admin,
}

class Principal(BaseModel):
    id: int
    type: Literal["member", "client", "admin"]

async def load_principal(
    db: AsyncSession,
    principal: Principal,
):
    model = PRINCIPAL_MODELS.get(principal.type)

    if model is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid principal type",
        )

    result = await db.execute(
        select(model).where(
            model.id == principal.id
        )
    )

    identity = result.scalar_one_or_none()

    if not identity or not identity.is_active:
        raise HTTPException(
            status_code=401,
            detail="Account unavailable",
        )

    return identity