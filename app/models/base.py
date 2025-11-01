from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Integer, Column, DateTime, func

class TimestampMixin:
    """Миксин для автоматического добавления временных меток в модели"""
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


@as_declarative()
class Base:
    """Базовая модель с автоматическим добавлением имени таблицы"""

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # автоматическое создание имени таблицы