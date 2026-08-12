import asyncio
from app.core.database import engine, Base
import app.models  # Imports all models

async def init_database():
    print("⚡ Connecting to Supabase PostgreSQL and creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Supabase PostgreSQL Database tables created successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_database())
