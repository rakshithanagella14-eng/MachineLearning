-- ── CREATE TABLES ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT,
    city        TEXT,
    age         INTEGER
);

CREATE TABLE IF NOT EXISTS Products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    price        REAL
);

CREATE TABLE IF NOT EXISTS Orders (
    order_id       INTEGER PRIMARY KEY,
    customer_id    INTEGER,
    order_date     TEXT,
    payment_method TEXT
);

CREATE TABLE IF NOT EXISTS OrderItems (
    item_id          INTEGER PRIMARY KEY,
    order_id         INTEGER,
    product_id       INTEGER,
    quantity         INTEGER,
    discount_percent REAL
);

-- ── INSERT DATA ──────────────────────────────────────────────

INSERT INTO Customers VALUES (1, 'Ravi Kumar',  'Hyderabad', 28);
INSERT INTO Customers VALUES (2, 'Sneha Reddy', 'Bangalore', 34);
INSERT INTO Customers VALUES (3, 'Arjun Mehta', 'Mumbai',    45);
INSERT INTO Customers VALUES (4, 'Priya Singh', 'Delhi',     22);
INSERT INTO Customers VALUES (5, 'Kiran Babu',  'Chennai',   67);
INSERT INTO Customers VALUES (6, 'Anjali Rao',  'Pune',      71);
INSERT INTO Customers VALUES (7, 'Vikram Das',  'Kolkata',   30);

INSERT INTO Products VALUES (1, 'Laptop',     'Electronics', 75000);
INSERT INTO Products VALUES (2, 'Phone',      'Electronics', 25000);
INSERT INTO Products VALUES (3, 'Tablet',     'Electronics', 30000);
INSERT INTO Products VALUES (4, 'Headphones', 'Audio',        5000);
INSERT INTO Products VALUES (5, 'Smartwatch', 'Wearables',   12000);
INSERT INTO Products VALUES (6, 'Speaker',    'Audio',        8000);
INSERT INTO Products VALUES (7, 'Keyboard',   'Accessories',  3000);

INSERT INTO Orders VALUES (101, 1, '2024-01-15', 'UPI');
INSERT INTO Orders VALUES (102, 2, '2024-02-20', 'Credit Card');
INSERT INTO Orders VALUES (103, 3, '2024-03-10', 'Debit Card');
INSERT INTO Orders VALUES (104, 4, '2024-04-05', 'COD');
INSERT INTO Orders VALUES (105, 5, '2024-05-01', 'UPI');
INSERT INTO Orders VALUES (106, 1, '2024-06-12', 'Net Banking');
INSERT INTO Orders VALUES (107, 6, '2024-07-18', 'Credit Card');

INSERT INTO OrderItems VALUES (1, 101, 1, 2, 10);
INSERT INTO OrderItems VALUES (2, 101, 4, 3,  5);
INSERT INTO OrderItems VALUES (3, 102, 2, 1, 15);
INSERT INTO OrderItems VALUES (4, 103, 3, 2,  0);
INSERT INTO OrderItems VALUES (5, 104, 5, 4, 20);
INSERT INTO OrderItems VALUES (6, 105, 6, 2, 10);
INSERT INTO OrderItems VALUES (7, 106, 7, 5,  0);
INSERT INTO OrderItems VALUES (8, 107, 1, 1, 25);

-- ============================================================
-- 1. GROUP BY - Single Column
-- ============================================================

-- Total orders per payment method
SELECT payment_method,
       COUNT(order_id) AS total_orders
FROM Orders
GROUP BY payment_method;

-- Total revenue per product category
SELECT p.category,
       SUM(p.price * oi.quantity) AS total_revenue
FROM Products p
JOIN OrderItems oi ON p.product_id = oi.product_id
GROUP BY p.category;

-- ============================================================
-- 2. GROUP BY - Multiple Columns
-- ============================================================

-- Orders per customer per month
SELECT c.name,
       strftime('%m', o.order_date) AS month,
       COUNT(o.order_id)            AS total_orders
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.name, month;

-- ============================================================
-- 3. HAVING Clause
-- ============================================================

-- Categories where total revenue > 50000
SELECT p.category,
       SUM(p.price * oi.quantity) AS total_revenue
FROM Products p
JOIN OrderItems oi ON p.product_id = oi.product_id
GROUP BY p.category
HAVING SUM(p.price * oi.quantity) > 50000;

-- Payment methods used more than once
SELECT payment_method,
       COUNT(order_id) AS total_orders
FROM Orders
GROUP BY payment_method
HAVING COUNT(order_id) > 1;

-- Products with average discount greater than 10%
SELECT p.product_name,
       AVG(oi.discount_percent) AS avg_discount
FROM Products p
JOIN OrderItems oi ON p.product_id = oi.product_id
GROUP BY p.product_name
HAVING AVG(oi.discount_percent) > 10;

-- ============================================================
-- 4. INNER JOIN
-- ============================================================

-- Customer names with their order details
SELECT c.name,
       o.order_id,
       o.order_date,
       o.payment_method
FROM Customers c
INNER JOIN Orders o ON c.customer_id = o.customer_id;

-- ============================================================
-- 5. LEFT JOIN
-- ============================================================

-- All customers including those with NO orders (Vikram Das → NULL)
SELECT c.name,
       c.city,
       o.order_id,
       o.order_date
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id;

-- ============================================================
-- 6. RIGHT JOIN (simulated with LEFT JOIN swap)
-- ============================================================

-- All orders with customer details
SELECT c.name,
       c.city,
       o.order_id,
       o.payment_method
FROM Orders o
LEFT JOIN Customers c ON o.customer_id = c.customer_id;

-- ============================================================
-- 7. JOIN 3 Tables
-- ============================================================

-- Full order details: Customer + Order + Product
SELECT c.name,
       p.product_name,
       p.category,
       oi.quantity,
       p.price,
       (p.price * oi.quantity) AS total_cost
FROM Customers c
JOIN Orders     o  ON c.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id    = oi.order_id
JOIN Products   p  ON oi.product_id = p.product_id;

-- ============================================================
-- 8. JOIN + GROUP BY + HAVING (Combined)
-- ============================================================

-- High-spending customers who spent more than 50000
SELECT c.name,
       SUM(p.price * oi.quantity) AS total_spent
FROM Customers c
JOIN Orders     o  ON c.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id    = oi.order_id
JOIN Products   p  ON oi.product_id = p.product_id
GROUP BY c.name
HAVING SUM(p.price * oi.quantity) > 50000;
