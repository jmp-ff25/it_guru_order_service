from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Index, func, Table
from sqlalchemy.orm import relationship
from app.models import Base

# Таблица связи M:N между номенклатурой и категориями
nomenclature_categories = Table(
    'nomenclature_categories',
    Base.metadata,
    Column('nomenclature_id', Integer, ForeignKey('nomenclature.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Category(Base):
    """Модель категории товаров с поддержкой иерархии (adjacency list)"""
    __tablename__ = "categories"
    
    name = Column(String(255), nullable=False, comment="Название категории")
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True, comment="ID родительской категории")
    slug = Column(String(255), unique=True, nullable=False, comment="Уникальный slug для URL")
    
    # Связи будут добавлены позже
    
    # Уникальность имени в рамках одного родителя (без учета регистра)
    __table_args__ = (
        Index(
            "uq_category_name_parent",
            func.lower(name),
            parent_id,
            unique=True
        ),
    )

class Nomenclature(Base):
    """Модель номенклатуры (товаров)"""
    
    sku = Column(String(100), unique=True, nullable=False, comment="Артикул товара")
    name = Column(String(255), nullable=False, comment="Название товара") 
    price = Column(Numeric(10, 2), nullable=False, comment="Текущая цена")
    quantity = Column(Integer, nullable=False, default=0, comment="Остаток на складе")
    
    # Связи будут добавлены позже