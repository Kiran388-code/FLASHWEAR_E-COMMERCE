import asyncio
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session_maker, engine, Base
from app.models import Category, Brand, User

async def seed_database():
    print("⚡ Connecting to Supabase PostgreSQL for Seeding Categories & System Data...")
    
    # 1. Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_maker() as session:
        # Seed Categories
        categories_data = [
            Category(id=1, name="Men's Western Wear", slug="mens-western", description="Men casuals, shirts, jeans", image_url="https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=300", is_active=True),
            Category(id=2, name="Women's Dresses & Tops", slug="womens-western", description="Women dresses and tops", image_url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=300", is_active=True),
            Category(id=3, name="Men's Ethnic Wear", slug="mens-ethnic", description="Festive kurtas and suits", image_url="https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=300", is_active=True),
            Category(id=4, name="Women's Ethnic & Sarees", slug="womens-ethnic", description="Anarkali suits and sarees", image_url="https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=300", is_active=True),
            Category(id=5, name="Unisex Hoodies & Jackets", slug="unisex-casuals", description="Oversized hoodies and jackets", image_url="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=300", is_active=True)
        ]
        for cat in categories_data:
            existing = await session.get(Category, cat.id)
            if not existing:
                session.add(cat)

        # Seed Brands
        brands_data = [
            Brand(id=1, name="FlashWear Originals", slug="flashwear", logo_url="https://example.com/logo.png", description="In-house brand", is_active=True),
            Brand(id=2, name="Levi's", slug="levis", logo_url="https://example.com/levis.png", description="Denim apparel", is_active=True),
            Brand(id=3, name="Zara", slug="zara", logo_url="https://example.com/zara.png", description="Fast fashion dresses", is_active=True),
            Brand(id=4, name="Manyavar", slug="manyavar", logo_url="https://example.com/manyavar.png", description="Ethnic fashion", is_active=True),
            Brand(id=5, name="Biba", slug="biba", logo_url="https://example.com/biba.png", description="Women ethnic suits", is_active=True)
        ]
        for brd in brands_data:
            existing = await session.get(Brand, brd.id)
            if not existing:
                session.add(brd)

        # Seed Users
        users_data = [
            User(id=1, email="customer@flashwear.com", hashed_password="$2b$12$k0BEmV7woyWaMRvnF6Hu0ehtMchRozTNszlrUZN.A89oCdLJyQwFm", full_name="Kiran Customer", role="customer", is_active=True),
            User(id=2, email="admin@flashwear.com", hashed_password="$2b$12$k0BEmV7woyWaMRvnF6Hu0ehtMchRozTNszlrUZN.A89oCdLJyQwFm", full_name="System Admin", role="admin", is_active=True)
        ]
        for usr in users_data:
            existing = await session.get(User, usr.id)
            if not existing:
                session.add(usr)

        await session.commit()
        print("✅ Supabase PostgreSQL ready: Categories, brands, and system users initialized. Products remain 0 until added manually by Sellers.")

if __name__ == "__main__":
    asyncio.run(seed_database())
