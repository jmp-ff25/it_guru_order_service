from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.models import Base, TimestampMixin

class Order(Base):
    """Модель заказа"""
    
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, comment="ID клиента")
    status = Column(String(50), nullable=False, default="created", comment="Статус заказа: created/paid/shipped/completed/cancelled")
    
    # Связи
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """Модель позиции заказа (связь заказ-товар с количеством и исторической ценой)"""
    
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    nomenclature_id = Column(Integer, ForeignKey("nomenclature.id"), nullable=False)
    quantity = Column(Integer, nullable=False, comment="Количество товара в заказе")
    price_at_order = Column(Numeric(10, 2), nullable=False, comment="Цена товара на момент заказа")
    
    # Связи
    order = relationship("Order", back_populates="items")
    nomenclature = relationship("Nomenclature")
    
    # Ограничения
    __table_args__ = (
        CheckConstraint(quantity > 0, name="chk_order_item_quantity_positive"),
    )