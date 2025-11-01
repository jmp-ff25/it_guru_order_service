# 🚀 Быстрое развертывание IT Guru Order Service

## Одной командой (рекомендуется)
```bash
git clone <repository-url> && \
cd 3.order_service && \
docker-compose up -d && \
sleep 10 && \
docker exec -it server_it_guru alembic upgrade head && \
bash scripts/load_mock_data.sh && \
echo "✅ Готово! Swagger UI: http://localhost:8075/docs"
```

## Пошагово

### 1. Клонирование
```bash
git clone <repository-url>
cd 3.order_service
```

### 2. Запуск контейнеров
```bash
docker-compose up -d
```

### 3. Миграции
```bash
docker exec -it server_it_guru alembic upgrade head
```

### 4. Тестовые данные (опционально)
```bash
bash scripts/load_mock_data.sh
```

### 5. Проверка
- Swagger UI: http://localhost:8075/docs
- Приложение: http://localhost:8075
- База данных: `localhost:5440`

## Быстрые команды

```bash
# Статус контейнеров
docker-compose ps

# Логи приложения
docker-compose logs -f server_it_guru

# Подключение к БД
docker exec -it postgres_server psql -U postgres -d consult_db

# Перезапуск сервиса
docker-compose restart server_it_guru

# Полный сброс
docker-compose down && docker-compose up -d
```

## Troubleshooting

**Порт занят?** Измените порты в `docker-compose.yml`:
```yaml
ports:
  - "8076:8000"  # вместо 8075:8000
  - "5441:5432"  # вместо 5440:5432  
```

**Ошибка подключения к БД?** Подождите ~10 сек и повторите миграции.