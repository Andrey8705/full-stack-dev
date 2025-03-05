CREATE INDEX idx_cars_brand_model ON cars(brand,model);
CREATE INDEX idx_cars_year ON cars(year);
CREATE INDEX idx_cars_price ON cars(price);
CREATE INDEX idx_client_id ON clients(id);

CREATE INDEX idx_cars_id ON cars(id);
CREATE INDEX idx_cars_year_price ON cars(year,price);
CREATE INDEX idx_sales_car_id ON sales(car_id);

EXPLAIN SELECT c.*
FROM cars c
JOIN sales s ON c.id = s.car_id
WHERE c.year > 2020
AND c.price < 10000000;
