SELECT 
    c.first_name as client_name,
    c.last_name as client_last_name,
    car.brand as car_brand,
    car.model as car_model,
    s.sale_date as sale_date,
    s.amount as amount

FROM 
    sales s
LEFT JOIN cars car ON s.car_id = car.id
LEFT JOIN clients c ON s.client_id = c.id;

SELECT
    c.first_name as client_name,
    c.last_name as client_last_name,
    COUNT(s.id) as sales_count
FROM
    clients c
LEFT JOIN sales s ON c.id = s.client_id
GROUP BY
    c.first_name,
    c.last_name;

SELECT 
    e.first_name as employee_name,
    e.last_name as employee_last_name,
    e.position as employee_position,
    COUNT(s.id) as sales_count,
    s.amount as amount
FROM employees e
LEFT JOIN sales s ON e.id = s.employee_id
GROUP BY
    e.first_name,
    e.last_name,
    e.position,
    s.amount;

SELECT 
    car.brand as car_brand,
    car.model as car_model,
    COUNT(s.id) as sales_count,
    COALESCE(SUM(s.amount), 0) as total_amount --команда COALESCE преобразует NULL в 0

FROM cars car
LEFT JOIN sales s ON car.id = s.car_id
GROUP BY
    car.brand,
    car.model
ORDER BY
    total_amount DESC;


