"""
Утилиты безопасности: генерация API ключей, аутентификация
"""
import secrets
from fastapi import Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.client import Client
from app.core.db import AsyncSessionLocal


def generate_api_key() -> str:
    """
    Генерирует случайный уникальный API ключ.
    
    Returns:
        Строка вида 'gen_' + 32 hex символа
    """
    random_part = secrets.token_hex(16)  # 32 символа
    return f"gen_{random_part}"


async def get_current_client(
    x_api_key: str = Header(..., description="API ключ для аутентификации")
) -> Client:
    """
    Dependency для получения текущего авторизованного клиента по API ключу.
    
    Args:
        x_api_key: Значение заголовка X-API-Key
        
    Returns:
        Объект клиента из БД
        
    Raises:
        HTTPException 401: Если ключ неверный или клиент не найден
    """
    session: AsyncSession = AsyncSessionLocal()
    try:
        stmt = select(Client).where(Client.api_key == x_api_key)
        result = await session.execute(stmt)
        client = result.scalars().first()
        
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return client
    finally:
        await session.close()
