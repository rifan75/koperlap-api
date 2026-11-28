import secrets
import hashlib
import json

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.principal import Principal, load_principal
from app.core.auth.pkce import verify_pkce
from app.core.rbac.service import get_user_authorities
from app.core.auth.token import issue_token_pair, rotate_refresh_token


AUTH_CODE_EXPIRE = 60

def hash_code(code: str) -> str:
    return hashlib.sha256(
        code.encode()
    ).hexdigest()


async def create_authorization_code(
    redis: Redis,
    principal: Principal,
    state: str,
    code_challenge: str,
    code_challenge_method: str = "S256",
) -> str:

    if code_challenge_method != "S256":
        raise ValueError("Only S256 is supported")

    if len(code_challenge) != 43:
        raise ValueError("Invalid code challenge")

    code = secrets.token_urlsafe(32)

    key = f"auth:code:{hash_code(code)}"

    payload = {
        "principal": principal.model_dump(mode="json"),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    stored = await redis.set(
        key,
        json.dumps(payload),
        ex=AUTH_CODE_EXPIRE,
        nx=True,
    )

    if not stored:
        raise RuntimeError(
            "Could not create authorization code"
        )

    return code


async def authorize(
    redis: Redis,
    db: AsyncSession,
    code: str,
    verifier: str,
):

    # 1. Retrieve authorization code
    key = f"auth:code:{hash_code(code)}"

    raw_payload = await redis.get(key)

    if not raw_payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authorization code",
        )

    if isinstance(raw_payload, bytes):
        raw_payload = raw_payload.decode("utf-8")

    try:
        authorization = json.loads(raw_payload)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization code payload",
        )

    # 2. Verify PKCE
    if authorization.get("code_challenge_method") != "S256":
        raise HTTPException(
            status_code=401,
            detail="Unsupported PKCE method",
        )

    if not verify_pkce(
        verifier,
        authorization["code_challenge"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid PKCE verifier",
        )

    # 3. Atomically consume authorization code
    consumed = await redis.eval(
        """
        local value = redis.call('GET', KEYS[1])

        if value == ARGV[1] then
            redis.call('DEL', KEYS[1])
            return 1
        end

        return 0
        """,
        1,
        key,
        raw_payload,
    )

    if not consumed:
        raise HTTPException(
            status_code=401,
            detail="Authorization code already used",
        )

    try:
        # 4. Reconstruct principal
        principal = Principal(
            **authorization["principal"]
        )

        # 5. Validate account
        identity = await load_principal(
            db,
            principal,
        )

        if not identity:
            raise HTTPException(
                status_code=401,
                detail="Account unavailable",
            )

        # 6. Resolve RBAC
        roles, permissions = await get_user_authorities(
            db,
            principal,
        )

        # 7. Create session and issue tokens
        tokens = await issue_token_pair(
            db=db,
            principal=principal,
            roles=roles,
            permissions=permissions,
        )

        # 8. Persist session and refresh token
        await db.commit()

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "expires_in": tokens["expires_in"],
            "user": {
                "id": str(principal.id),
                "type": principal.type,
                "roles": roles,
                "permissions": permissions,
            },
        }

    except Exception:
        await db.rollback()
        raise


async def refresh_authorization(
    db: AsyncSession,
    refresh_token: str,
):
    try:
        result = await rotate_refresh_token(
            db=db,
            raw_token=refresh_token,
        )

        # Commit rotation or reuse-detection revocation
        await db.commit()

    except Exception:
        await db.rollback()
        raise

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )

    if result.get("reuse_detected"):
        raise HTTPException(
            status_code=401,
            detail="Refresh token reuse detected. Session revoked.",
        )

    return result