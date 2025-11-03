"""
Сервис для работы с заказами
"""
from fastapi import Response, HTTPException, status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

from app.services.base import BaseService
from app.models.order import Order, OrderItem
from app.models.nomenclature import Nomenclature
from app.models.client import Client
from app.dto.base import BaseResponseModel
from app.dto.order import AddItemRequest, OrderResponse, OrderItemResponse


class OrderService:
    """Сервис для управления заказами"""

    @BaseService.with_session
    async def add_item_to_order(
        order_id: int,
        request: AddItemRequest,
        current_client: Client,
        response: Response,
        session: AsyncSession
    ) -> BaseResponseModel[OrderResponse]:
        """
        Добавляет товар в заказ или увеличивает его количество.
        
        Args:
            order_id: ID заказа
            request: Данные о товаре и количестве
            current_client: Текущий авторизованный клиент
            response: FastAPI Response объект
            session: Сессия БД (инжектится декоратором)
            
        Returns:
            BaseResponseModel с полным заказом
            
        Raises:
            HTTPException 404: Заказ или товар не найден
            HTTPException 403: Заказ принадлежит другому клиенту
            HTTPException 423: Заказ заблокирован (статус не позволяет изменения)
            HTTPException 409: Недостаточно товара на складе
        """
        # 1. Получаем заказ с позициями
        stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        order = (await session.execute(stmt)).scalar_one_or_none()
        
        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        # 2. Проверяем принадлежность заказа текущему клиенту
        if order.client_id != current_client.id:
            raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="You can only modify your own orders"
            )
        
        # 3. Проверяем статус заказа (редактировать можно только created)
        if order.status != "created":
            raise HTTPException(
                status_code=http_status.HTTP_423_LOCKED,
                detail=f"Cannot modify order with status '{order.status}'. Only 'created' orders can be modified."
            )
        
        # 4. Получаем товар с блокировкой строки (защита от race condition)
        stmt = select(Nomenclature).where(
            Nomenclature.id == request.nomenclature_id
        ).with_for_update()
        
        nomenclature = (await session.execute(stmt)).scalar_one_or_none()
        
        if not nomenclature:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"Product {request.nomenclature_id} not found"
            )
        
        # 5. Проверяем наличие товара на складе
        if nomenclature.quantity < request.quantity:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail=f"Insufficient stock. Available: {nomenclature.quantity}, requested: {request.quantity}"
            )
        
        # 6. Ищем существующую позицию в заказе
        existing_item = None
        for item in order.items:
            if item.nomenclature_id == request.nomenclature_id:
                existing_item = item
                break
        
        if existing_item:
            # Товар уже есть в заказе — увеличиваем количество
            new_quantity = existing_item.quantity + request.quantity
            
            # Проверяем что хватит товара для нового количества
            if nomenclature.quantity < request.quantity:
                raise HTTPException(
                    status_code=http_status.HTTP_409_CONFLICT,
                    detail=f"Insufficient stock for total quantity. Available: {nomenclature.quantity}"
                )
            
            existing_item.quantity = new_quantity
            nomenclature.quantity -= request.quantity
            
        else:
            # Создаём новую позицию в заказе
            new_item = OrderItem(
                order_id=order_id,
                nomenclature_id=request.nomenclature_id,
                quantity=request.quantity,
                price_at_order=nomenclature.price
            )
            session.add(new_item)
            nomenclature.quantity -= request.quantity
        
        # 7. Сохраняем изменения (commit выполнит декоратор)
        await session.flush()
        
        # 8. Формируем ответ с полным заказом
        await session.refresh(order, ["items"])
        
        # Считаем общую сумму заказа
        total_amount = Decimal(0)
        items_response = []
        
        for item in order.items:
            total_price = item.price_at_order * item.quantity
            total_amount += total_price
            
            items_response.append(OrderItemResponse(
                id=item.id,
                nomenclature_id=item.nomenclature_id,
                quantity=item.quantity,
                unit_price=item.price_at_order,
                total_price=total_price
            ))
        
        order_data = OrderResponse(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            items=items_response,
            total_amount=total_amount
        )
        
        return await OrderService.format_response(
            response=response,
            data=order_data,
            message="Item added to order successfully"
        )

    @staticmethod
    async def format_response(
        response: Response,
        data: OrderResponse | None,
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
