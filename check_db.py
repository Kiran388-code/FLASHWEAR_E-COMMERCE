import asyncio
from sqlalchemy import text
from app.core.database import engine

async def inspect_supabase_database():
    print("=" * 60)
    print("⚡ FLASHWEAR SUPABASE POSTGRESQL DATABASE INSPECTOR")
    print("=" * 60)
    
    async with engine.connect() as conn:
        # 1. List all public tables
        tables_res = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
        tables = [row[0] for row in tables_res.fetchall()]
        
        print("\n📊 Database Tables:")
        if not tables:
            print("  (No tables found in public schema)")
        for table in sorted(tables):
            count_res = await conn.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
            count = count_res.scalar()
            print(f"  • {table.ljust(25)} -> {count} records")
            
        print("\n🔍 Product Catalog Sample:")
        try:
            products_res = await conn.execute(text('SELECT id, name, price, sku FROM products LIMIT 5'))
            products = products_res.fetchall()
            if not products:
                print("  (No products inserted yet)")
            for p in products:
                print(f"  • #{p[0]}: {p[1]} (₹{p[2]}) - SKU: {p[3]}")
        except Exception as e:
            print(f"  (Products table not queried: {e})")

    print("=" * 60)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(inspect_supabase_database())
