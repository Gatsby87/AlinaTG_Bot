import pytest
from ai.memory_manager import MemoryManager
from ai.ai_client import AIClient

@pytest.mark.asyncio
async def test_memory_creation():
    """Тест создания памяти"""
    ai_client = AIClient()
    memory_manager = MemoryManager(ai_client)
    
    # Мокаем AI клиент
    with patch.object(ai_client, 'generate_response') as mock_ai:
        mock_ai.return_value = "Имя: Тест. Интересы: программирование. Настроение: хорошее. Ключевые темы: технологии."
        
        memory = await memory_manager._create_initial_memory("Привет, меня зовут Тест, я люблю программирование")
        
        assert "Тест" in memory
        assert "программирование" in memory

@pytest.mark.asyncio
async def test_memory_update(db_session):
    """Тест обновления памяти"""
    from models.user import User
    ai_client = AIClient()
    memory_manager = MemoryManager(ai_client)
    
    # Создаем пользователя с существующей памятью
    user = User(
        id=123, 
        username="test_user",
        memory_summary="Имя: Тест. Интересы: программирование."
    )
    db_session.add(user)
    await db_session.commit()
    
    with patch.object(ai_client, 'generate_response') as mock_ai:
        mock_ai.return_value = "Имя: Тест. Интересы: программирование, музыка. Настроение: отличное."
        
        new_memory = await memory_manager.update_user_memory(
            db_session, 123, "Сегодня слушаю музыку, настроение отличное!"
        )
        
        assert "музыка" in new_memory
        assert "отличное" in new_memory