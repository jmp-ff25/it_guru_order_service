"""
Маршруты для аутентификации и регистрации клиентов
"""
from fastapi import APIRouter, Response, Depends

from app.dto.base import BaseResponseModel
from app.dto.auth import RegisterRequest, RegisterResponseData, ClientMeData
from app.services.auth_service import AuthService
from app.core.security import get_current_client
from app.models.client import Client

router = APIRouter()


@router.post(
    "/register",
    description=(
        "Регистрирует нового клиента в системе. "
        "Принимает имя и адрес, генерирует уникальный API ключ для дальнейшей аутентификации. "
        "API ключ необходимо сохранить на стороне клиента для использования в заголовке X-API-Key."
    ),
    response_model=BaseResponseModel[RegisterResponseData],
    status_code=200
)
async def register_client(
    request: RegisterRequest,
    response: Response
):
    """
    Регистрация нового клиента
    
    - **name**: Имя клиента (обязательно, 1-255 символов)
    - **address**: Адрес клиента (опционально)
    
    Возвращает сгенерированный API ключ для аутентификации
    """
    return await AuthService.register(request=request, response=response)


@router.get(
    "/me",
    description=(
        "Возвращает данные текущего авторизованного клиента. "
        "Требует передачи API ключа в заголовке X-API-Key."
    ),
    response_model=BaseResponseModel[ClientMeData],
    status_code=200
)
async def get_client_profile(
    response: Response,
    current_client: Client = Depends(get_current_client)
):
    """
    Получение данных текущего клиента (личный кабинет)
    
    Требует аутентификации через заголовок X-API-Key
    """
    return await AuthService.get_me(current_client, response)
