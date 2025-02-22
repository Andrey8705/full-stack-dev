SELECT * 
FROM cars c1
WHERE price > (
    SELECT AVG(c2.price) 
    FROM cars c2
    WHERE c2.brand = c1.brand
);

SELECT first_name AS client_name
FROM clients
WHERE id IN (
    SELECT client_id
    FROM sales
    GROUP BY client_id
    HAVING COUNT(client_id) > 2
)
ORDER BY (
    SELECT COUNT(s.client_id) 
    FROM sales s 
    WHERE s.client_id = clients.id
) DESC;


CREATE VIEW sales_by_month AS
SELECT 
    car.brand, 
    TO_CHAR(s.sale_date, 'YYYY-MM') AS sale_month,
    COUNT(*) AS sales_count
FROM sales s
LEFT JOIN cars car ON car.id = s.car_id
GROUP BY car.brand, sale_month;

SELECT s.sale_date  --Оставил этот запрос, чтобы видеть продажи по месяцам
FROM sales s;

SELECT * FROM sales_by_month --Создал представление чтобы искать самые популярные марки машины по месяцам.
WHERE sale_month = '2024-02'
ORDER BY sales_count DESC
LIMIT 1;

CREATE VIEW sales_report AS
SELECT 
    DATE_TRUNC('month', s.sale_date) AS sale_month,
    COUNT(s.id) AS total_sales, --Количество продаж
    SUM(s.amount) AS total_revenue, --Вся выручка
    AVG(s.amount) AS avg_check --Средний чек
FROM sales s
GROUP BY sale_month
ORDER BY sale_month DESC;

SELECT * FROM sales_report;

CREATE VIEW active_clients AS
SELECT c.id AS client_id, c.first_name, c.last_name, c.email
FROM clients c
JOIN sales s ON c.id = s.client_id
WHERE s.sale_date >= CURRENT_DATE - INTERVAL '8 months'
ORDER BY s.sale_date DESC;

SELECT * FROM active_clients; --Нет активных клиентов за последние 3 месяца. Для наглядности изменил интервал на 9 месяцев.

CREATE VIEW managers_performance AS
SELECT 
    e.id AS manager_id, 
    e.first_name || ' ' || e.last_name AS manager_name,
    COUNT(s.id) AS total_sales,         -- Количество продаж
    SUM(s.amount) AS total_revenue,     -- Общая выручка
    ROUND(100.0 * COUNT(s.id) / NULLIF(COUNT(DISTINCT s.client_id), 0), 2) AS conversion_rate -- Конверсия
FROM employees e
LEFT JOIN sales s ON e.id = s.employee_id
WHERE e.position IN ('Manager', 'Менеджер продаж', 'Старший менеджер')
GROUP BY e.id, manager_name
ORDER BY total_sales DESC;

SELECT * FROM managers_performance;


