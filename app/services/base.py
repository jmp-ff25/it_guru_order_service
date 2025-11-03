"""
Базовый класс для сервисов с декоратором управления сессией БД
"""
from functools import wraps
from app.core.db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Базовый класс для всех сервисов приложения"""

    @staticmethod
    def with_session(fn):
        """
        Декоратор для автоматического управления сессией БД.
        Создаёт сессию, передаёт её в функцию, коммитит и закрывает.
        В случае ошибки откатывает транзакцию.
        """
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            session: AsyncSession = AsyncSessionLocal()
            try:
                result = await fn(*args, session=session, **kwargs)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
        return wrapper
