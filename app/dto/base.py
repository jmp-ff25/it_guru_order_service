"""
Базовые модели ответов API
"""
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel


T = TypeVar('T')


class BaseResponseModel(BaseModel, Generic[T]):
    """
    Универсальная обёртка для всех ответов API.
    
    Attributes:
        success: Флаг успешности операции
        message: Текстовое сообщение (описание результата или ошибки)
        data: Полезная нагрузка ответа (типизированная)
    """
    success: bool
    message: str
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {}
            }
        }
