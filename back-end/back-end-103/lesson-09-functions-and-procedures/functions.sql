CREATE OR REPLACE FUNCTION calculate_total_price(
    brand varchar(30),
    model varchar(30),
    climate boolean,
    leather boolean
)
RETURNS INTEGER AS $$
DECLARE
    total INTEGER;
BEGIN

    SELECT c.price INTO total 
    FROM cars c 
    WHERE c.brand = calculate_total_price.brand AND c.model = calculate_total_price.model 
    LIMIT 1;

    IF total IS NULL THEN 
        RAISE EXCEPTION 'Автомобиль % % не найден', brand, model;
    END IF;

    IF climate THEN
        total := total + 500000;
    END IF;
    IF leather THEN
        total := total + 800000;
    END IF;

    RETURN total;
END;
$$ LANGUAGE plpgsql;

SELECT calculate_total_price('Lada', 'Vesta', true, true);
SELECT calculate_total_price('BMW', 'X5', true, false);
SELECT calculate_total_price('Tesla', 'X5', true, false);
SELECT calculate_total_price('Mazda', 'RX300', true, true);
SELECT calculate_total_price('Aston Martin', '-', true, true);
SELECT calculate_total_price('Toyota', 'Camry', true, false);
SELECT calculate_total_price('Hyundai', 'Accent', true, false);

CREATE OR REPLACE FUNCTION available_cars(
    brand_param varchar(30),
    model_param varchar(30),
    year_param integer,
    climate boolean,
    leather boolean
)
RETURNS TABLE (brand varchar(30), model varchar(30), price integer) AS $$ 
DECLARE
    car_status TEXT;
    car_price INTEGER;
BEGIN
    SELECT c.brand, c.model, c.price, c.status 
    INTO brand, model, car_price, car_status
    FROM cars c 
    WHERE c.brand = brand_param 
      AND c.model = model_param 
      AND c.year = year_param
    LIMIT 1;

    IF car_status = 'Под заказ' THEN
        RAISE EXCEPTION 'Автомобиля % % нет в наличии', brand_param, model_param;
    END IF;

    IF brand IS NULL OR model IS NULL THEN
        RAISE EXCEPTION 'Автомобиль % % не найден', brand_param, model_param;
    END IF;

    RETURN QUERY SELECT brand, model, car_price;
END;
$$ LANGUAGE plpgsql;


SELECT available_cars('Lada', 'Vesta', 2015, true, false);
SELECT available_cars('BMW', 'X5', 2020, true, false);
SELECT available_cars('Tesla', 'X5', 2025, true, false);
SELECT available_cars('Mazda', 'RX300', 2018, true, true);
SELECT available_cars('Aston Martin', '-', 2000, true, true);
SELECT available_cars('Toyota', 'Camry', 2024, true, false);
SELECT available_cars('Hyundai', 'Accent', 2023, true, false);


CREATE OR REPLACE FUNCTION sales_analysis(
    start_date DATE,
    end_date DATE
)
RETURNS TABLE (sale_date DATE, total_sales NUMERIC) AS $$ 
BEGIN
    RETURN QUERY 
    SELECT s.sale_date, COALESCE(SUM(s.amount), 0)::NUMERIC AS total_sales
    FROM sales s
    WHERE s.sale_date BETWEEN start_date AND end_date
    GROUP BY s.sale_date
    ORDER BY s.sale_date;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM sales_analysis('2024-01-01', '2024-12-31');


CREATE OR REPLACE FUNCTION calculate_commission(
    manager_id INTEGER,
    start_date DATE,
    end_date DATE,
    commission_rate NUMERIC
)
RETURNS NUMERIC AS $$ 
DECLARE
    total_sales NUMERIC := 0;
    commission_amount NUMERIC := 0;
BEGIN
    SELECT COALESCE(SUM(s.amount), 0) INTO total_sales
    FROM sales s
    WHERE s.employee_id = manager_id
      AND s.sale_date BETWEEN start_date AND end_date;

    commission_amount := total_sales * (commission_rate / 100);

    RETURN commission_amount;
END;
$$ LANGUAGE plpgsql;

SELECT calculate_commission(1, '2024-01-01', '2024-12-31', 0.05);

