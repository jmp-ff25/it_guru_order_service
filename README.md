# IT Guru Order Service

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)

Микросервис для управления заказами в системе IT Guru. Построен на FastAPI с асинхронной архитектурой и PostgreSQL.

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт) | 📄 [QUICKSTART.md](./QUICKSTART.md)
- [Архитектура](#-архитектура)
- [База данных](#-база-данных) | 📄 [database/README.md](./database/README.md)
- [API Endpoints](#-api-endpoints)
- [Разработка](#-разработка)
- [Тестирование](#-тестирование)

## 🚀 Быстрый старт

### Требования

- Docker >= 24.0
- Docker Compose >= 2.0
- Git

### Развертывание

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd 3.order_service
   ```

2. **Запуск контейнеров**
   ```bash
   docker-compose up -d
   ```
   
   Это запустит:
   - PostgreSQL (порт 5440)
   - FastAPI приложение (порт 8075)

3. **Применение миграций**
   ```bash
   docker exec -it server_it_guru alembic upgrade head
   ```

4. **Загрузка тестовых данных** (опционально)
   ```bash
   bash scripts/load_mock_data.sh
   ```

5. **Проверка работоспособности**
   ```bash
   curl http://localhost:8075/docs
   ```

### Быстрая команда (всё в одном)
```bash
docker-compose up -d && \
docker exec -it server_it_guru alembic upgrade head && \
bash scripts/load_mock_data.sh
```

## 🏗️ Архитектура

### Структура проекта
```
3.order_service/
├── app/                    # Основной код приложения
│   ├── core/              # Конфигурация и общие утилиты
│   │   ├── config.py      # Настройки приложения
│   │   └── db.py          # Подключение к БД
│   ├── models/            # SQLAlchemy модели
│   │   ├── base.py        # Базовые классы
│   │   ├── client.py      # Модель клиента
│   │   ├── nomenclature.py # Товары и категории
│   │   └── order.py       # Заказы и позиции
│   ├── repositories/      # Слой доступа к данным
│   ├── services/          # Бизнес-логика
│   ├── schemas/           # Pydantic схемы
│   └── __main__.py        # Точка входа FastAPI
├── database/              # Управление базой данных
│   ├── seeds/             # Тестовые данные
│   └── README.md          # Документация БД
├── migrations/            # Alembic миграции
├── scripts/               # Утилиты и скрипты
├── dockerfiles/           # Docker конфигурация
├── docker-compose.yml     # Оркестрация контейнеров
└── README.md              # Этот файл
```

### Технологический стек
- **Backend**: FastAPI 0.104+ (Python 3.11)
- **База данных**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.x (async)
- **Миграции**: Alembic
- **Валидация**: Pydantic v2
- **Контейнеризация**: Docker + Docker Compose

## 🗄️ База данных

### Схема данных
- **categories** - Иерархия категорий товаров
- **nomenclature** - Каталог товаров с ценами и остатками
- **nomenclature_categories** - Связь M:N товары↔категории  
- **client** - Клиенты системы
- **order** - Заказы клиентов
- **orderitem** - Позиции заказов

### Управление данными

#### Миграции
```bash
# Просмотр статуса
docker exec -it server_it_guru alembic current

# Применение миграций
docker exec -it server_it_guru alembic upgrade head

# Откат миграций  
docker exec -it server_it_guru alembic downgrade base

# Создание новой миграции
docker exec -it server_it_guru alembic revision --autogenerate -m "Description"
```

#### Тестовые данные
```bash
# Загрузка тестовых данных (рекомендуется)
bash scripts/load_mock_data.sh

# Или напрямую через SQL
docker exec -i postgres_server psql -U postgres -d consult_db < database/seeds/mock_data.sql

# Просмотр данных
docker exec -i postgres_server psql -U postgres -d consult_db < database/seeds/show_data.sql

# Очистка данных
docker exec -i postgres_server psql -U postgres -d consult_db < database/seeds/clear_data.sql
```

#### Подключение к БД
```bash
# Консоль PostgreSQL
docker exec -it postgres_server psql -U postgres -d consult_db

# Список таблиц
docker exec postgres_server psql -U postgres -d consult_db -c "\\dt"

# Быстрая статистика
docker exec postgres_server psql -U postgres -d consult_db -c "
SELECT 'Категорий' as info, COUNT(*) FROM categories
UNION ALL SELECT 'Товаров', COUNT(*) FROM nomenclature  
UNION ALL SELECT 'Заказов', COUNT(*) FROM \"order\";
"
```

## 🔌 API Endpoints

После запуска сервиса доступны:

- **Swagger UI**: http://localhost:8075/docs
- **ReDoc**: http://localhost:8075/redoc  
- **OpenAPI JSON**: http://localhost:8075/api/openapi.json

### Основные эндпоинты
```
POST /orders/{id}/items   # Добавление товара в заказ
GET  /orders/{id}         # Получение заказа
PUT  /orders/{id}/status  # Изменение статуса заказа
```

## 🔧 Разработка

### Локальная разработка
```bash
# Перезапуск только приложения
docker-compose restart server_it_guru

# Просмотр логов
docker-compose logs -f server_it_guru

# Вход в контейнер для отладки
docker exec -it server_it_guru bash
```

### Переменные окружения

Основные настройки в `app/.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@postgres_server:5432/consult_db
ENVIRONMENT=development
DEBUG=True
```

### Полезные команды
```bash
# Полная пересборка
docker-compose down && docker-compose up --build -d

# Сброс базы данных
docker exec -it server_it_guru alembic downgrade base
docker exec -it server_it_guru alembic upgrade head
bash scripts/load_mock_data.sh

# Проверка состояния контейнеров
docker-compose ps
```

## 🧪 Тестирование

### Доступные тестовые данные

После загрузки `mock_data.sql` доступны:
- **10 категорий** с иерархией (Электроника → Смартфоны/Ноутбуки/Наушники)
- **14 товаров** с реалистичными ценами (iPhone, Samsung, MacBook, и др.)
- **5 клиентов** из разных городов
- **3 заказа** в статусах: created, paid, shipped
- **6 позиций** в заказах с товарами

### Примеры API запросов

```bash
# Получить заказ #1 (Иван Петров)
curl http://localhost:8075/orders/1

# Добавить товар в заказ
curl -X POST http://localhost:8075/orders/1/items \
  -H "Content-Type: application/json" \
  -d '{"nomenclature_id": 2, "quantity": 1}'
```

## 📝 Разработческие заметки

### Архитектурные принципы
- **Clean Architecture** - разделение на слои (models, repositories, services)
- **Dependency Injection** - через FastAPI Depends
- **Async/Await** - полностью асинхронная архитектура
- **Type Safety** - строгая типизация с Pydantic

### Коммерческие практики

#### Управление данными по средам
```bash
# Development - тестовые данные
bash scripts/load_mock_data.sh

# Testing - фикстуры для автотестов  
docker exec -i postgres_server psql -U postgres -d test_db < database/fixtures/test_data.sql

# Staging - копия продакшена (обезличенная)
pg_dump production_db | pg_restore staging_db

# Production - реальные данные + резервные копии
pg_dump consult_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Стратегия безопасности данных
- **Тестовые данные** - в репозитории (не содержат PII)
- **Staging данные** - обезличенные копии продакшена
- **Production данные** - зашифрованные бэкапы вне репозитория
- **Секреты** - через Docker secrets или Kubernetes secrets

#### Масштабирование подхода
```bash
# Маленькие проекты - простые SQL файлы
database/seeds/mock_data.sql

# Средние проекты - модульная структура
database/seeds/
├── 01_references.sql    # Справочники
├── 02_users.sql        # Пользователи  
├── 03_products.sql     # Товары
└── 04_orders.sql       # Заказы

# Большие проекты - программные сидеры
database/seeders/
├── ReferenceSeeder.py
├── UserSeeder.py
└── ProductSeeder.py
```

### Подход к данным

#### Философия разделения
- **Миграции** (`migrations/`) - только структура БД (DDL: CREATE, ALTER, DROP)
- **Seed данные** (`database/seeds/`) - тестовые данные для разработки
- **Бизнес-данные** - через API, админку или отдельные скрипты



### Безопасность
- Валидация входных данных через Pydantic
- SQL Injection protection через SQLAlchemy
- Проверка существования сущностей перед операциями

## 🐛 Траблшутинг

### Частые проблемы

**Контейнер не запускается**
```bash
docker-compose logs server_it_guru
docker-compose ps
```

**База данных недоступна**
```bash
docker exec postgres_server pg_isready -U postgres
docker-compose restart postgres_server
```

**Ошибки миграций**
```bash
# Проверить состояние
docker exec -it server_it_guru alembic current

# Сбросить до чистого состояния  
docker exec -it server_it_guru alembic downgrade base
docker exec -it server_it_guru alembic upgrade head
```

**Порты заняты**
```bash
# Изменить порты в docker-compose.yml
ports:
  - "8076:8000"  # FastAPI
  - "5441:5432"  # PostgreSQL
```

