import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import settings
from core.database import init_db
from core.logger import setup_logger
from bot.dispatcher import setup_dispatcher
from web.app import create_app

async def main():
    """Главная функция запуска бота и веб-сервера"""
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        # Инициализация базы данных
        await init_db()
        logger.info("Database initialized successfully")
        
        # Создание бота
        bot = Bot(
            token=settings.TELEGRAM_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Настройка диспетчера
        dp = setup_dispatcher(bot)
        
        # Создание FastAPI приложения
        web_app = create_app(bot)
        
        logger.info("Starting bot and web server...")
        
        # Запуск бота и веб-сервера
        await asyncio.gather(
            dp.start_polling(bot),
            web_app_task(web_app)
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

async def web_app_task(web_app):
    """Задача для запуска веб-сервера"""
    import uvicorn
    config = uvicorn.Config(
        app=web_app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())