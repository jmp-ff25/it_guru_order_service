-- =====================================================
-- IT Guru Order Service - Просмотр данных
-- =====================================================
-- Этот скрипт показывает обзор всех загруженных данных
-- =====================================================

\echo '🔍 IT Guru Order Service - Обзор данных'
\echo ''

-- Статистика по таблицам
\echo '📊 ОБЩАЯ СТАТИСТИКА:'
SELECT 
    'Категорий' as "Тип данных", 
    COUNT(*)::text as "Количество"
FROM categories
UNION ALL
SELECT 'Товаров', COUNT(*)::text FROM nomenclature  
UNION ALL
SELECT 'Клиентов', COUNT(*)::text FROM client
UNION ALL
SELECT 'Заказов', COUNT(*)::text FROM "order"
UNION ALL  
SELECT 'Позиций заказов', COUNT(*)::text FROM orderitem
UNION ALL
SELECT 'Связей товар-категория', COUNT(*)::text FROM nomenclature_categories;

\echo ''
\echo '📂 КАТЕГОРИИ С ИЕРАРХИЕЙ:'
SELECT 
    c1.id,
    c1.name as "Категория",
    COALESCE(c2.name, '(корневая)') as "Родитель",
    c1.slug as "URL"
FROM categories c1 
LEFT JOIN categories c2 ON c1.parent_id = c2.id
ORDER BY COALESCE(c1.parent_id, 0), c1.id;

\echo ''  
\echo '📦 ТОВАРЫ ПО КАТЕГОРИЯМ:'
SELECT 
    c.name as "Категория",
    n.sku as "Артикул", 
    n.name as "Товар",
    n.price as "Цена",
    n.quantity as "Остаток"
FROM nomenclature n
JOIN nomenclature_categories nc ON n.id = nc.nomenclature_id
JOIN categories c ON nc.category_id = c.id  
ORDER BY c.id, n.sku;

\echo ''
\echo '🛒 ЗАКАЗЫ КЛИЕНТОВ:'
SELECT 
    o.id as "№ заказа",
    c.name as "Клиент", 
    o.status as "Статус",
    COUNT(oi.id) as "Позиций",
    SUM(oi.quantity * oi.price_at_order) as "Сумма"
FROM "order" o
JOIN client c ON o.client_id = c.id
LEFT JOIN orderitem oi ON o.id = oi.order_id  
GROUP BY o.id, c.name, o.status
ORDER BY o.id;

\echo ''
\echo '📋 ДЕТАЛИ ЗАКАЗОВ:'  
SELECT 
    o.id as "№ заказа",
    n.sku as "Артикул",
    n.name as "Товар",
    oi.quantity as "Кол-во", 
    oi.price_at_order as "Цена",
    (oi.quantity * oi.price_at_order) as "Сумма"
FROM orderitem oi
JOIN "order" o ON oi.order_id = o.id
JOIN nomenclature n ON oi.nomenclature_id = n.id
ORDER BY o.id, oi.id;