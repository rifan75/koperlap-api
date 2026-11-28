from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.core.auth.service import authenticate_admin, LoginRequest, AuthorizeRequest
from app.database.dependencies import get_db
from app.core.auth.authorization import create_authorization_code
from app.core.principal import Principal
from app.core.redis import get_redis
from app.core.dependencies import get_current_token
from app.core.session import revoke_session
from app.config import settings

from app.core.auth.token import rotate_refresh_token


router = APIRouter()


@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    # 1. Authenticate admin
    admin = await authenticate_admin(
        db,
        data.email,
        data.password,
    )

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    # 2. Check account status
    if not admin.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive",
        )

    # 3. Construct principal
    principal = Principal(
        id=admin.id,
        type="admin",
    )

    # 4. Create authorization code
    try:
        code = await create_authorization_code(
            redis=redis,
            principal=principal,
            state=data.state,
            code_challenge=data.code_challenge,
            code_challenge_method=data.code_challenge_method,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "code": code,
        "state": data.state,
    }

@router.post("/logout")
async def logout(
    payload: dict = Depends(get_current_token),
    db: AsyncSession = Depends(get_db),
):
    session_id = UUID(payload["session_id"])

    await revoke_session(
        db=db,
        session_id=session_id,
    )

    await db.commit()

    return {
        "message": "Successfully logged out"
    }