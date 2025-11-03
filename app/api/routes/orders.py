"""
Маршруты для работы с заказами
"""
from fastapi import APIRouter, Response, Depends

from app.dto.base import BaseResponseModel
from app.dto.order import AddItemRequest, OrderResponse
from app.services.order_service import OrderService
from app.core.security import get_current_client
from app.models.client import Client

router = APIRouter()


@router.post(
    "/{order_id}/items",
    description=(
        "Добавляет товар в заказ. "
        "Если товар уже есть в заказе, его количество увеличивается. "
        "Если товара нет на складе в нужном количестве — возвращается ошибка. "
        "Требует аутентификации через X-API-Key."
    ),
    response_model=BaseResponseModel[OrderResponse],
    status_code=200,
    responses={
        200: {"description": "Товар успешно добавлен в заказ"},
        404: {"description": "Заказ или товар не найден"},
        403: {"description": "Заказ принадлежит другому клиенту"},
        423: {"description": "Заказ заблокирован для изменений (уже оплачен/отправлен)"},
        409: {"description": "Недостаточно товара на складе"},
    }
)
async def add_item_to_order(
    order_id: int,
    request: AddItemRequest,
    response: Response,
    current_client: Client = Depends(get_current_client)
):
    """
    Добавление товара в заказ
    
    - **order_id**: ID заказа (в URL)
    - **nomenclature_id**: ID товара из номенклатуры
    - **quantity**: Количество товара (целое число > 0)
    
    Возвращает полный заказ со всеми позициями и общей суммой.
    
    Бизнес-правила:
    - Заказ должен принадлежать текущему клиенту
    - Заказ должен быть в статусе 'created'
    - Товара должно быть достаточно на складе
    - Если товар уже в заказе — количество увеличивается
    """
    return await OrderService.add_item_to_order(
        order_id=order_id,
        request=request,
        current_client=current_client,
        response=response
    )
