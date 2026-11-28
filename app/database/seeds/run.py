
import asyncio

from app.database import AsyncSessionLocal
from app.database.seeds.oauth_clients import seed_oauth_clients


async def main():
    async with AsyncSessionLocal() as db:
        await seed_oauth_clients(db)

    print("OAuth clients seeded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
