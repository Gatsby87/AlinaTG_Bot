from aiogram import Dispatcher
from bot.telegram_handler import TelegramHandler

def setup_dispatcher(bot) -> Dispatcher:
    """Настройка диспетчера"""
    dp = Dispatcher()
    
    # Инициализация обработчиков
    telegram_handler = TelegramHandler(bot)
    
    # Включение роутера
    dp.include_router(telegram_handler.router)
    
    return dp