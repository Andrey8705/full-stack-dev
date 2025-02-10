UPDATE cars
SET 
    status = 'Со скидкой'
WHERE 
    year < 2020 AND status = 'В наличии';

UPDATE cars
SET price = price * 0.95
WHERE status = 'Со скидкой';

UPDATE clients
SET
    phone = '98845534815'
WHERE
    id = 5;

ALTER TABLE sales
ADD COLUMN status VARCHAR(255);

UPDATE sales
SET
    status = 'Завершена'
WHERE
    sale_date < CURRENT_DATE - INTERVAL '1 month';

DELETE FROM clients
WHERE NOT EXISTS (
    select 1 from sales
    where sales.client_id = clients.id);
