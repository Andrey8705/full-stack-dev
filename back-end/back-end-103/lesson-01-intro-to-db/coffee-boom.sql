CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL categories(id),
    status BOOLEAN NOT NULL DEFAULT TRUE,
    date_added TIMESTAMP NOT NULL DEFAULT NOW()
)

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    registration_date TIMESTAMP NOT NULL DEFAULT NOW(),
    number_of_bonus_points INT NOT NULL DEFAULT 0
)

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL customers(id),
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    date_added TIMESTAMP NOT NULL DEFAULT NOW(),
    payment_method VARCHAR(20) NOT NULL
)

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL orders(id),
    product_id INT NOT NULL products(id),
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
)

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)

INSERT INTO categories (name) VALUES ("Coffee")
INSERT INTO categories (name) VALUES ("Snacks")
INSERT INTO categories (name) VALUES ("Desserts")
INSERT INTO categories (name) VALUES ("Snacks")

INSERT INTO products (name, description, price, category_id, status) VALUES ("Espresso", "Strong coffee", 2.50, 1, TRUE)
INSERT INTO products (name, description, price, category_id, status) VALUES ("Cappuccino", "Coffee with milk", 3.50, 1, TRUE)
INSERT INTO products (name, description, price, category_id, status) VALUES ("Latte", "Coffee with milk", 3.50, 1, TRUE)
INSERT INTO products (name, description, price, category_id, status) VALUES ("Muffin", "Chocolate muffin", 2.00, 2, TRUE)
INSERT INTO products (name, description, price, category_id, status) VALUES ("Croissant", "Butter croissant", 1.50, 2, TRUE)

INSERT INTO customers (first_name, last_name, email, phone) VALUES ("John", "Doe", "John@gmail.com", "123456789")
INSERT INTO customers (first_name, last_name, email, phone) VALUES ("Jane", "Doe", "Jane@gmail.com", "987654321")

INSERT INTO orders (customer_id, total_price, payment_method) VALUES (1, 5.00, "cash")
INSERT INTO orders (customer_id, total_price, payment_method) VALUES (2, 3.50, "card")

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (1, 1, 2, 5.00)
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (2, 2, 1, 3.50)