"""
Сервис аутентификации и управления клиентами
"""
from fastapi import Response, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.base import BaseService
from app.models.client import Client
from app.dto.base import BaseResponseModel
from app.dto.auth import RegisterRequest, RegisterResponseData, ClientMeData
from app.core.security import generate_api_key


class AuthService:
    """Сервис для регистрации и аутентификации клиентов"""

    @BaseService.with_session
    async def register(
        request: RegisterRequest,
        response: Response,
        session: AsyncSession
    ) -> BaseResponseModel[RegisterResponseData]:
        """
        Регистрирует нового клиента и генерирует для него API ключ.
        
        Args:
            request: Данные для регистрации (имя, адрес)
            response: FastAPI Response объект для установки статус-кода
            session: Сессия БД (инжектится декоратором)
            
        Returns:
            BaseResponseModel с данными нового клиента и API ключом
        """
        # Генерируем уникальный API ключ
        api_key = generate_api_key()
        
        # Проверяем уникальность ключа (на всякий случай, хотя вероятность коллизии ~0)
        while True:
            stmt = select(Client).where(Client.api_key == api_key)
            existing = (await session.execute(stmt)).scalars().first()
            if not existing:
                break
            api_key = generate_api_key()
        
        # Создаём нового клиента
        new_client = Client(
            name=request.name,
            address=request.address,
            api_key=api_key
        )
        
        session.add(new_client)
        await session.flush()  # Получаем ID до коммита
        
        # Формируем ответ
        data = RegisterResponseData(
            client_id=new_client.id,
            name=new_client.name,
            api_key=api_key
        )
        
        return await AuthService.format_response(
            response=response,
            data=data,
            message="Client registered successfully"
        )

    @staticmethod
    async def get_me(
        client: Client,
        response: Response
    ) -> BaseResponseModel[ClientMeData]:
        """
        Возвращает данные текущего авторизованного клиента.
        
        Args:
            client: Текущий клиент (из dependency get_current_client)
            response: FastAPI Response объект
            
        Returns:
            BaseResponseModel с данными клиента
        """
        data = ClientMeData(
            id=client.id,
            name=client.name,
            address=client.address
        )
        
        return await AuthService.format_response(
            response=response,
            data=data,
            message="Client data retrieved"
        )

    @staticmethod
    async def format_response(
        response: Response,
        data: RegisterResponseData | ClientMeData | None,
        message: str = ""
    ) -> BaseResponseModel:
        """
        Форматирует стандартный ответ API.
        
        Args:
            response: FastAPI Response для установки статус-кода
            data: Полезная нагрузка ответа
            message: Текстовое сообщение
            
        Returns:
            BaseResponseModel с флагом успеха и данными
        """
        response.status_code = http_status.HTTP_200_OK
        return BaseResponseModel(
            success=True,
            message=message,
            data=data
        )
