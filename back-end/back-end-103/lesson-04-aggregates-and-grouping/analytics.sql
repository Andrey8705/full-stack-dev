SELECT
  brand,
  COUNT(*) as total_cars,
  AVG(price) as avg_price,
  SUM(price) as total_value
FROM cars
GROUP BY brand
HAVING COUNT(*) > 1;


SELECT brand, COUNT(*) AS total_cars
FROM cars
GROUP BY brand
ORDER BY total_cars DESC;

SELECT year, AVG(price) AS avg_price
FROM cars
GROUP BY year
ORDER BY year ASC;

SELECT c.brand, COUNT(*) AS total_sales
FROM sales s
JOIN cars c ON s.car_id = c.id
GROUP BY c.brand
ORDER BY total_sales DESC
LIMIT 1;

SELECT 
    DATE_TRUNC('month', s.sale_date) AS sale_month,
    SUM(c.price) AS total_sales_amount
FROM sales s
JOIN cars c ON s.car_id = c.id
GROUP BY sale_month
ORDER BY sale_month ASC;

SELECT 
    s.employee_id, 
    COUNT(*) AS total_sales
FROM sales s
GROUP BY s.employee_id
ORDER BY total_sales DESC;
