from fastapi import APIRouter

# Главный роутер для API
main_router = APIRouter(prefix="/api/v1")

# Здесь будут подключены роутеры для клиентов, заказов и номенклатуры
# main_router.include_router(clients_router)
# main_router.include_router(orders_router)
# main_router.include_router(nomenclature_router)