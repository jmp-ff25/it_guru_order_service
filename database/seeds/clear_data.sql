-- =====================================================
-- IT Guru Order Service - Очистка тестовых данных
-- =====================================================
-- Этот скрипт удаляет все данные из таблиц,
-- сохраняя структуру и сбрасывая автоинкременты
-- =====================================================

BEGIN;

-- Удаляем данные в правильном порядке (учитывая FK)
TRUNCATE 
    orderitem,
    "order", 
    nomenclature_categories,
    nomenclature,
    categories,
    client
RESTART IDENTITY CASCADE;

COMMIT;

-- Показываем результат
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '🧹 Все тестовые данные удалены!';
    RAISE NOTICE '';
    RAISE NOTICE '📊 Текущее состояние:';
    RAISE NOTICE '   📂 Категорий: %', (SELECT COUNT(*) FROM categories);
    RAISE NOTICE '   📦 Товаров: %', (SELECT COUNT(*) FROM nomenclature);
    RAISE NOTICE '   👥 Клиентов: %', (SELECT COUNT(*) FROM client);
    RAISE NOTICE '   🛒 Заказов: %', (SELECT COUNT(*) FROM "order");
    RAISE NOTICE '   📋 Позиций заказов: %', (SELECT COUNT(*) FROM orderitem);
    RAISE NOTICE '';
END $$;