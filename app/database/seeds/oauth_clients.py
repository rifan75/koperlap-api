
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.models import OAuthClient


OAUTH_CLIENTS = [
    {
        "client_id": "koperlap-member",
        "client_secret_hash": None,
        "client_type": "public",
        "redirect_uris": [
            "http://localhost:3000/auth/callback",
            "http://localhost:8000/auth/callback",
        ],
        "allowed_scopes": [
            "openid",
            "profile",
            "email",
        ],
        "is_active": True,
    },
    {
        "client_id": "koperlap-client",
        "client_secret_hash": None,
        "client_type": "public",
        "redirect_uris": [
            "http://localhost:3000/auth/callback",
            "http://localhost:8000/auth/callback",
        ],
        "allowed_scopes": [
            "openid",
            "profile",
            "email",
        ],
        "is_active": True,
    },
    {
        "client_id": "koperlap-admin",
        "client_secret_hash": None,
        "client_type": "confidential",
        "redirect_uris": [
            "http://localhost:3000/auth/callback",
            "http://localhost:8000/auth/callback",
        ],
        "allowed_scopes": [
            "openid",
            "profile",
            "email",
            "admin",
        ],
        "is_active": True,
    },
]


async def seed_oauth_clients(db: AsyncSession):
    for client_data in OAUTH_CLIENTS:
        result = await db.execute(
            select(OAuthClient).where(
                OAuthClient.client_id == client_data["client_id"]
            )
        )

        existing_client = result.scalar_one_or_none()

        if existing_client:
            for key, value in client_data.items():
                setattr(existing_client, key, value)
        else:
            db.add(OAuthClient(**client_data))

    await db.commit()
