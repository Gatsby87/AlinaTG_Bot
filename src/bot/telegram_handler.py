from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.subscription_manager import SubscriptionManager
from bot.referral_manager import ReferralManager
from bot.filters import SubscriptionFilter, RateLimitFilter
from ai.ai_client import AIClient
from ai.memory_manager import MemoryManager
from core.database import get_db

class UserStates(StatesGroup):
    waiting_for_message = State()

class TelegramHandler:
    """Обработчик Telegram сообщений"""
    
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()
        self.ai_client = AIClient()
        self.subscription_manager = SubscriptionManager()
        self.referral_manager = ReferralManager()
        self.memory_manager = MemoryManager(self.ai_client)
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков"""
        # Команды
        self.router.message.register(self.start_handler, CommandStart())
        self.router.message.register(self.subscribe_handler, Command("subscribe"))
        self.router.message.register(self.status_handler, Command("status"))
        self.router.message.register(self.reset_handler, Command("reset"))
        self.router.message.register(self.referral_handler, Command("referral"))
        self.router.message.register(self.buy_handler, Command("buy"))
        
        # Текстовые сообщения
        self.router.message.register(
            self.message_handler, 
            F.text,
            SubscriptionFilter(),
            RateLimitFilter()
        )
    
    async def start_handler(self, message: Message, state: FSMContext):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        referral_code = message.text.split()[1] if len(message.text.split()) > 1 else None
        
        async for session in get_db():
            # Регистрация пользователя
            await self.subscription_manager.register_user(
                session, user_id, message.from_user.first_name
            )
            
            # Обработка реферальной ссылки
            if referral_code:
                await self.referral_manager.process_referral(
                    session, user_id, referral_code
                )
            
            # Проверка подписки
            has_access = await self.subscription_manager.check_subscription(
                session, user_id
            )
        
        if has_access:
            from ai.personality import Personality
            await message.answer(Personality.get_greeting())
        else:
            await self.send_trial_message(message)
        
        await state.set_state(UserStates.waiting_for_message)
    
    async def message_handler(self, message: Message, state: FSMContext):
        """Обработчик текстовых сообщений"""
        user_id = message.from_user.id
        
        async for session in get_db():
            # Обновление памяти
            memory = await self.memory_manager.update_user_memory(
                session, user_id, message.text
            )
            
            # Генерация ответа
            response = await self.ai_client.generate_response(
                message.text, 
                memory
            )
        
        await message.answer(response)
    
    async def subscribe_handler(self, message: Message):
        """Обработчик команды подписки"""
        user_id = message.from_user.id
        
        async for session in get_db():
            payment_url = await self.subscription_manager.create_subscription(
                session, user_id
            )
        
        if payment_url:
            await message.answer(
                f"Для оформления подписки перейди по ссылке:\n{payment_url}\n\n"
                f"Подписка даст тебе неограниченное общение со мной! 💫"
            )
        else:
            await message.answer("Произошла ошибка при создании платежа. Попробуй позже.")
    
    async def status_handler(self, message: Message):
        """Обработчик команды статуса"""
        user_id = message.from_user.id
        
        async for session in get_db():
            status = await self.subscription_manager.get_subscription_status(
                session, user_id
            )
        
        await message.answer(status)
    
    async def reset_handler(self, message: Message):
        """Обработчик сброса памяти"""
        user_id = message.from_user.id
        
        async for session in get_db():
            from models.user import User
            user = await session.get(User, user_id)
            if user:
                user.memory_summary = ""
                await session.commit()
        
        await message.answer("Память сброшена! Давай начнем общение заново 🌟")
    
    async def referral_handler(self, message: Message):
        """Обработчик реферальной системы"""
        user_id = message.from_user.id
        
        async for session in get_db():
            referral_link = await self.referral_manager.get_referral_link(
                session, user_id
            )
        
        await message.answer(
            f"Пригласи друзей и получай +1 день подписки за каждого! 🎁\n\n"
            f"Твоя реферальная ссылка:\n{referral_link}\n\n"
            f"Когда друг перейдет по ссылке и начнет общение, "
            f"твоя подписка автоматически продлится!"
        )
    
    async def buy_handler(self, message: Message):
        """Алиас для команды подписки"""
        await self.subscribe_handler(message)
    
    async def send_trial_message(self, message: Message):
        """Отправка сообщения о пробном периоде"""
        from ai.personality import Personality
        
        await message.answer(
            Personality.get_greeting() + "\n\n"
            "У тебя есть 1 день пробного периода, чтобы познакомиться со мной поближе! "
            "Если понравится наше общение, можешь оформить подписку командой /subscribe 🌸"
        )