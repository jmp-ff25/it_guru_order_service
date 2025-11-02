from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.router import main_router
from app.core.logger import logger

# Инициализация FastAPI
app = FastAPI(
    title=settings.app_title,
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# События старта и завершения
@app.on_event("startup")
async def startup():
    logger.info("🚀 Order Service запущен")
    logger.info(f"Зарегистрированные маршруты: {len(app.routes)}")
    # Инициализация БД будет происходить через Alembic миграции

@app.on_event("shutdown")
async def shutdown():
    logger.info("⏳ Завершение работы Order Service")

# Подключаем главный роутер
app.include_router(main_router)