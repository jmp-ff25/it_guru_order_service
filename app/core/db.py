# Database configuration and connection
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.pool import NullPool

DATABASE_URL = settings.database_url  # Читаем из конфига адрес подключения к БД

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session             # Отдаём сессию в обработчик, но не коммитим
        except Exception:
            await session.rollback()  # Откатываем транзакцию при ошибке
            raise
        finally:
            await session.close()     # Закрываем сессию