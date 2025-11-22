from typing import List, Dict

class TokenOptimizer:
    """Оптимизатор использования токенов"""
    
    def __init__(self, max_history_length: int = 10):
        self.max_history_length = max_history_length
    
    def optimize_conversation_history(self, history: List[Dict]) -> List[Dict]:
        """Оптимизация истории разговора"""
        if len(history) <= self.max_history_length:
            return history
        
        # Оставляем первые 2 сообщения и последние N сообщений
        keep_first = 2
        keep_last = self.max_history_length - keep_first
        
        optimized = history[:keep_first] + history[-keep_last:]
        return optimized
    
    def truncate_message(self, message: str, max_tokens: int = 150) -> str:
        """Обрезка сообщения до максимального количества токенов"""
        words = message.split()
        if len(words) <= max_tokens:
            return message
        
        truncated = ' '.join(words[:max_tokens])
        if len(truncated) < len(message):
            truncated += "..."
            
        return truncated