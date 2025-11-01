#!/bin/bash
# =====================================================
# IT Guru Order Service - Скрипт загрузки тестовых данных
# =====================================================

set -e  # Останавливаться при ошибках

echo "🌱 Загрузка тестовых данных в базу данных..."
echo

# Проверяем что контейнер PostgreSQL запущен
if ! docker ps | grep -q "postgres_server"; then
    echo "❌ Контейнер postgres_server не запущен!"
    echo "   Сначала запустите: docker-compose up -d"
    exit 1
fi

# Проверяем что контейнер приложения запущен  
if ! docker ps | grep -q "server_it_guru"; then
    echo "❌ Контейнер server_it_guru не запущен!"
    echo "   Сначала запустите: docker-compose up -d"
    exit 1
fi

# Проверяем что миграции применены
echo "🔍 Проверяем состояние миграций..."
if ! docker exec -it server_it_guru alembic current 2>/dev/null | grep -q "dbe5a65fd262"; then
    echo "❌ Миграции не применены!"
    echo "   Сначала выполните: docker exec -it server_it_guru alembic upgrade head"
    exit 1
fi

echo "✅ Миграции применены"
echo

# Загружаем тестовые данные
echo "📊 Загружаем тестовые данные..."
docker exec -i postgres_server psql -U postgres -d consult_db < database/seeds/mock_data.sql

echo
echo "🎉 Тестовые данные успешно загружены!"
echo
echo "📋 Полезные команды:"
echo "   Просмотр данных: docker exec postgres_server psql -U postgres -d consult_db -c '\\dt'"
echo "   Очистка данных:  docker exec postgres_server psql -U postgres -d consult_db -c 'TRUNCATE categories, nomenclature, client, \"order\", orderitem, nomenclature_categories RESTART IDENTITY CASCADE;'"
echo