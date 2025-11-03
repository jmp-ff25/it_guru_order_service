from sqlalchemy import Column, Integer, String, Text, Index
from app.models import Base, TimestampMixin

class Client(Base):
    """Модель клиента"""
    
    name = Column(String(255), nullable=False, comment="Имя клиента")
    address = Column(Text, nullable=True, comment="Адрес клиента")
    api_key = Column(String(64), unique=True, nullable=True, comment="Уникальный API ключ для аутентификации")
    
    __table_args__ = (
        Index("ix_client_api_key", "api_key", unique=True),
    )