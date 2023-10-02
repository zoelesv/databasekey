-- Drop tables if they exist and their dependent objects
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
​
-- Create the 'customers' table
CREATE TABLE orders (
    order_id SERIAL NOT NULL,
    customer_id INTEGER,
    date_ordered DATE,
    date_delivered DATE,
    price REAL NOT NULL,
    units INTEGER DEFAULT 1,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
​
-- Create the 'orders' table with a foreign key reference to 'customers'
CREATE TABLE customers (
    customer_id SERIAL NOT NULL,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    email VARCHAR(30) NOT NULL,
    PRIMARY KEY (customer_id),
    UNIQUE (email)
);
​
-- Insert values into the 'customers' table
INSERT INTO customers VALUES
(0, 'zoe', 'le', '141_shopaholic@gmail.com'),
(1, 'max', 'sivolella', 'max_amazon_orders@gmail.com'),
(2, 'varsha', 'moturi', 'varsha_customer@gmail.com'),
(3, 'robert', 'clements', 'robert_c@gmail.com'),
(4, 'jeff', 'bezos', 'i_am_amazon@amazon.com');
​
-- Insert values into the 'orders' table
INSERT INTO orders VALUES
(0, 1, '2023-09-15', '2023-10-17', 300.0, 2),
(1, 0, '2023-02-17', '2023-02-20', 50.0, 1),
(2, 3, '2022-05-16', '2022-05-25', 100.0, 3);
​
-- Attempt to insert a duplicate record into the 'customers' table
-- This will fail due to the primary key constraint on the 'customer_id' column
INSERT INTO customers VALUES(4, 'elon', 'musk', 'its_x_not_twiiter@x.com');
​
INSERT INTO customers VALUES(6, 'elon', 'musk', 'its_x_not_twiiter@x.com');
​
-- Selecting email from the 'customers' table using a subquery and foreign key
SELECT email
FROM customers
WHERE customer_id = (SELECT customer_id FROM orders WHERE order_id = 2);
​
-- Attempt to delete records from the 'customers' table
-- This will fail because it has a constraint with orders table
DELETE FROM customers WHERE customer_id=3;
​
-- Attempt to insert another duplicate record with the same email
-- This will fail due to the unique constraint on the 'email' column
INSERT INTO customers VALUES (7, NULL, NULL, '141_shopaholic@gmail.com');
​
-- Add a unique constraint to the 'phone_number' column in the 'customers' table
ALTER TABLE customers ADD phone_number VARCHAR(13) UNIQUE;
​
-- Update phone numbers for specific customer records
UPDATE customers SET phone_number = '803-456-2342' WHERE customer_id=0;
UPDATE customers SET phone_number = '567-345-6753' WHERE customer_id=1;
UPDATE customers SET phone_number = '123-673-9876' WHERE customer_id=2;
-- This will also fail due to the unique constraint on the 'phone_number' column
UPDATE customers SET phone_number = '803-456-2342' WHERE customer_id=3;
​
-- Select all records from the 'customers' table
SELECT * FROM customers;
​
-- Select all records from the 'orders' table
SELECT * FROM orders;