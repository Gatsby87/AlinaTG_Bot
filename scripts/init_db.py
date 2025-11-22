import asyncio
from src.core.database import init_db
from src.core.logger import setup_logger

async def main():
    """Инициализация базы данных"""
    setup_logger()
    await init_db()
    print("База данных успешно инициализирована!")

if __name__ == "__main__":
    asyncio.run(main())