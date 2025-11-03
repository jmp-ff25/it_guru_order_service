"""
DTO модели для аутентификации и регистрации клиентов
"""
from pydantic import BaseModel, Field
from typing import Optional


class RegisterRequest(BaseModel):
    """Запрос на регистрацию нового клиента"""
    name: str = Field(..., min_length=1, max_length=255, description="Имя клиента")
    address: Optional[str] = Field(None, description="Адрес клиента")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Новый Клиент",
                "address": "г. Москва, ул. Примерная, д. 1, кв. 10"
            }
        }


class RegisterResponseData(BaseModel):
    """Данные ответа при успешной регистрации"""
    client_id: int = Field(..., description="ID созданного клиента")
    name: str = Field(..., description="Имя клиента")
    api_key: str = Field(..., description="Сгенерированный API ключ для аутентификации")

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": 6,
                "name": "Новый Клиент",
                "api_key": "gen_7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c"
            }
        }


class ClientMeData(BaseModel):
    """Данные клиента для эндпоинта /me"""
    id: int = Field(..., description="ID клиента")
    name: str = Field(..., description="Имя клиента")
    address: Optional[str] = Field(None, description="Адрес клиента")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Иван Петров",
                "address": "г. Москва, ул. Тверская, д. 15, кв. 42"
            }
        }
