from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from ai.ai_client import AIClient

class MemoryManager:
    """Менеджер памяти пользователя"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.max_summary_length = 400
    
    async def update_user_memory(
        self, 
        session: AsyncSession, 
        user_id: int,
        new_interaction: str
    ) -> str:
        """Обновление памяти пользователя на основе нового взаимодействия"""
        from models.user import User
        
        user = await session.get(User, user_id)
        if not user:
            return ""
        
        current_memory = user.memory_summary or ""
        
        # Если память пустая, создаем начальную
        if not current_memory:
            new_memory = await self._create_initial_memory(new_interaction)
        else:
            new_memory = await self._update_existing_memory(current_memory, new_interaction)
        
        # Обрезаем до максимальной длины
        if len(new_memory) > self.max_summary_length:
            new_memory = new_memory[:self.max_summary_length].rsplit(' ', 1)[0] + "..."
        
        user.memory_summary = new_memory
        await session.commit()
        
        return new_memory
    
    async def _create_initial_memory(self, interaction: str) -> str:
        """Создание начальной памяти"""
        prompt = f"""
        На основе этого сообщения пользователя выдели ключевую информацию:
        - Имя (если упомянуто)
        - Основные интересы/темы
        - Текущее настроение
        - Ключевые детали
        
        Сообщение: {interaction}
        
        Сформируй краткое описание (до 400 символов) в формате:
        "Имя: [имя]. Интересы: [интересы]. Настроение: [настроение]. Ключевые темы: [темы]."
        """
        
        # Используем AI для создания памяти
        return await self.ai_client.generate_response(prompt, "")
    
    async def _update_existing_memory(self, current_memory: str, new_interaction: str) -> str:
        """Обновление существующей памяти"""
        prompt = f"""
        Обнови описание пользователя на основе нового сообщения.
        
        Текущее описание: {current_memory}
        Новое сообщение: {new_interaction}
        
        Обнови информацию об интересах, настроении, ключевых темах.
        Сохрани формат и длину до 400 символов.
        """
        
        return await self.ai_client.generate_response(prompt, "")