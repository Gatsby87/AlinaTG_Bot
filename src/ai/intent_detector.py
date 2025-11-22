from typing import Dict, Any
import re

class IntentDetector:
    """Детектор намерений пользователя"""
    
    def __init__(self):
        self.patterns = {
            'greeting': [
                r'привет', r'здравствуй', r'добрый', r'хай', r'hello', r'hi'
            ],
            'farewell': [
                r'пока', r'до свидания', r'прощай', r'bye', r'goodbye'
            ],
            'thanks': [
                r'спасибо', r'благодарю', r'thanks', r'thank you'
            ],
            'subscription': [
                r'подписк', r'оплат', r'куп', r'продл', r'тариф'
            ],
            'problem': [
                r'проблем', r'беда', r'трудн', r'сложн', r'плохо'
            ],
            'support': [
                r'помоги', r'помощ', r'поддерж', r'совет'
            ]
        }
    
    def detect_intent(self, text: str) -> Dict[str, Any]:
        """Определение намерения пользователя"""
        text = text.lower()
        detected_intents = []
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    detected_intents.append(intent)
                    break
        
        return {
            'intents': detected_intents,
            'is_emergency': any(i in detected_intents for i in ['problem', 'support'])
        }