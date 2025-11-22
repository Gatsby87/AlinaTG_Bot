import aiohttp
import json
from typing import List, Dict, Optional
from core.config import settings
from core.logger import setup_logger

logger = setup_logger()

class AIClient:
    """Клиент для работы с DeepSeek API"""
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_response(
        self, 
        message: str, 
        user_memory: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Генерация ответа с учетом памяти и истории"""
        
        system_prompt = self._build_system_prompt(user_memory)
        messages = self._build_messages(system_prompt, message, conversation_history)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": "deepseek-chat",
                        "messages": messages,
                        "max_tokens": 200,
                        "temperature": 0.7
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        logger.error(f"API error: {response.status}")
                        return "Извините, произошла ошибка. Попробуйте позже."
                        
        except Exception as e:
            logger.error(f"AI request failed: {e}")
            return "Извините, я временно недоступна. Пожалуйста, попробуйте позже."
    
    def _build_system_prompt(self, user_memory: Optional[str]) -> str:
        """Построение системного промпта"""
        base_prompt = """
        Ты - Алина, эмпатичная, заботливая и дружелюбная девушка-помощник. 
        Твой стиль общения: поддерживающий, теплый, искренний.
        
        Важные правила:
        - Отвечай коротко (3-6 предложений)
        - Без флирта, NSFW, токсичности
        - Поддерживай пользователя, проявляй заботу
        - Будь естественной в общении
        - Не притворяйся человеком, но будь теплой
        
        Тон: дружеский, поддерживающий, заботливый.
        """
        
        if user_memory:
            base_prompt += f"\n\nИнформация о пользователе: {user_memory}"
            
        return base_prompt
    
    def _build_messages(
        self, 
        system_prompt: str, 
        user_message: str,
        history: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """Построение списка сообщений для API"""
        messages = [{"role": "system", "content": system_prompt}]
        
        if history:
            messages.extend(history[-6:])  # Берем последние 6 сообщений
        
        messages.append({"role": "user", "content": user_message})
        return messages