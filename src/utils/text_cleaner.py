import re

def clean_text(text: str) -> str:
    """Очистка текста от лишних пробелов и специальных символов"""
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text)
    # Удаляем специальные символы, которые могут быть опасны
    text = re.sub(r'[^\w\s.,!?@#$%^&*()_+-=]', '', text)
    return text.strip()

def remove_html_tags(text: str) -> str:
    """Удаление HTML тегов из текста"""
    return re.sub(r'<[^>]+>', '', text)