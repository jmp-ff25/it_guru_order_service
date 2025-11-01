from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Основные настройки приложения
    app_title: str = "IT Guru Order Service"
    secret_key: str = "your-secret-key-change-in-production"
    
    # База данных
    database_url: str
    
    # Настройки JWT (если планируется авторизация)
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Настройки CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Настройки логирования
    log_level: str = "INFO"
    
    # Настройки pydantic модели
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()