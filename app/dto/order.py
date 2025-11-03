"""
DTO модели для работы с заказами
"""
from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal


class AddItemRequest(BaseModel):
    """Запрос на добавление товара в заказ"""
    nomenclature_id: int = Field(..., gt=0, description="ID товара из номенклатуры")
    quantity: int = Field(..., gt=0, description="Количество товара (должно быть > 0)")

    class Config:
        json_schema_extra = {
            "example": {
                "nomenclature_id": 1,
                "quantity": 2
            }
        }


class OrderItemResponse(BaseModel):
    """Позиция заказа в ответе"""
    id: int = Field(..., description="ID позиции заказа")
    nomenclature_id: int = Field(..., description="ID товара")
    quantity: int = Field(..., description="Количество")
    unit_price: Decimal = Field(..., description="Цена за единицу на момент заказа")
    total_price: Decimal = Field(..., description="Общая стоимость позиции")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nomenclature_id": 1,
                "quantity": 2,
                "unit_price": 99999.99,
                "total_price": 199999.98
            }
        }


class OrderResponse(BaseModel):
    """Полный заказ с позициями"""
    id: int = Field(..., description="ID заказа")
    client_id: int = Field(..., description="ID клиента")
    status: str = Field(..., description="Статус заказа")
    items: List[OrderItemResponse] = Field(default_factory=list, description="Список позиций заказа")
    total_amount: Decimal = Field(..., description="Общая сумма заказа")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "client_id": 1,
                "status": "created",
                "items": [
                    {
                        "id": 1,
                        "nomenclature_id": 1,
                        "quantity": 2,
                        "unit_price": 99999.99,
                        "total_price": 199999.98
                    },
                    {
                        "id": 2,
                        "nomenclature_id": 7,
                        "quantity": 1,
                        "unit_price": 24999.99,
                        "total_price": 24999.99
                    }
                ],
                "total_amount": 224999.97
            }
        }
