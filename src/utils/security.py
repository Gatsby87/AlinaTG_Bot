import hashlib
import secrets

def generate_secure_token(length: int = 32) -> str:
    """Генерация безопасного токена"""
    return secrets.token_urlsafe(length)

def hash_data(data: str) -> str:
    """Хеширование данных"""
    return hashlib.sha256(data.encode()).hexdigest()

def verify_hash(data: str, hash_str: str) -> bool:
    """Проверка хеша"""
    return hash_data(data) == hash_str