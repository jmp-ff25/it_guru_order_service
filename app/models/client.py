from sqlalchemy import Column, Integer, String, Text
from app.models import Base, TimestampMixin

class Client(Base):
    """Модель клиента"""
    
    name = Column(String(255), nullable=False, comment="Имя клиента")
    address = Column(Text, nullable=True, comment="Адрес клиента")