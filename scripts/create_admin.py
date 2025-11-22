import asyncio
from src.core.database import AsyncSessionLocal
from src.core.config import settings
from src.web.auth import get_password_hash

async def create_admin():
    """Создание администратора"""
    # В этом проекте используется простой аутентификационный механизм
    # с проверкой логина и пароля из .env файла
    print("Администратор создается через переменные окружения:")
    print(f"Username: {settings.ADMIN_USERNAME}")
    print(f"Password: {'*' * len(settings.ADMIN_PASSWORD)}")
    print("Убедитесь, что переменные ADMIN_USERNAME и ADMIN_PASSWORD установлены в .env файле")

if __name__ == "__main__":
    asyncio.run(create_admin())