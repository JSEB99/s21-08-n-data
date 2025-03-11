-- TIME DIMENSION
INSERT INTO time_dim
(date_value, date_year, date_month, date_day, date_weekday, date_hour)
SELECT date_value, date_year, date_month, date_day, date_weekday, date_hour
FROM (
    SELECT DISTINCT
        date_trunc('hour', date_column) AS date_value,
        date_part('year', date_column) AS date_year,
        date_part('month', date_column) AS date_month,
        date_part('day', date_column) AS date_day,
        date_part('dow', date_column) AS date_weekday,
        date_part('hour', date_column) AS date_hour
    FROM (
        SELECT customer_order_date AS date_column FROM orders
        UNION
        SELECT shipping_date FROM orders
    ) AS unique_dates
) AS distinct_dates
ORDER BY date_value;
-- CUSTOMER DIMENSION
INSERT INTO customers_dim (
    customer_id,
    customer_first_name,
    customer_last_name,
    customer_type,
    customer_store_state,
    customer_store_city,
    customer_store_street,
    customer_store_zipcode,
    customer_store_latitude,
    customer_store_longitude
)
SELECT DISTINCT
    customer_id,
    customer_fname AS customer_first_name,
    customer_lname AS customer_last_name,
    customer_segment AS customer_type,
    customer_state AS customer_store_state,
    customer_city AS customer_store_city,
    customer_street AS customer_store_street,
    customer_zipcode AS customer_store_zipcode,
    latitude AS customer_store_latitude,
    longitude AS customer_store_longitude
FROM orders
ORDER BY customer_id ASC;
-- PRODUCTS DIMENSION
-- CATEGORY VALUES
INSERT INTO category_values (category_name)
SELECT DISTINCT category_name
FROM orders; 
-- DEPARTMENT VALUES
INSERT INTO department_values (department_name)
SELECT DISTINCT department_name
FROM orders;
-- PRODUCTS
INSERT INTO products_dim (product_id, product_name, product_price, category_id, department_id)
SELECT DISTINCT 
    o.product_card_id AS product_id,
    o.product_name,
    o.product_price,
    cv.category_id,  
    dv.department_id  
FROM orders o
JOIN category_values cv ON o.category_name = cv.category_name  
JOIN department_values dv ON o.department_name = dv.department_name;
-- ORDERS DIMENSION
INSERT INTO orders_dim (
    order_id, 
    order_status, 
    order_region, 
    order_country, 
    order_state, 
    order_city, 
    order_market, 
    order_shipping_mode, 
    order_delivery_status, 
    order_days_for_shipping_real, 
    order_days_for_shipment_scheduled, 
    order_late_delivery_risk, 
    order_payment_type
)
SELECT DISTINCT 
    order_id, 
    order_status, 
    order_region, 
    order_country, 
    order_state, 
    order_city, 
    market, 
    shipping_mode, 
    delivery_status, 
    days_for_shipping_real, 
    days_for_shipment_scheduled, 
    late_delivery_risk, 
    trans_type 
FROM orders
ORDER BY order_id;
-- FACTS TABLE - ORDER ITEM FACT TABLE
INSERT INTO order_facts (
    order_id,
    customer_id,
    product_id,
    time_order_dim_id,
    time_shipping_dim_id,
    order_item_quantity,
    order_item_discount,
    order_item_discount_rate,
    order_item_profit_ratio,
    order_item_total,
	order_profit_per_order,
	sales
)
SELECT 
    od.order_id,
    c.customer_id,
    p.product_id,
    t1.time_dim_id AS time_order_dim_id,
    t2.time_dim_id AS time_shipping_dim_id,
    SUM(o.order_item_quantity) AS total_quantity,
    AVG(o.order_item_discount) AS total_discount,
    AVG(o.order_item_discount_rate) AS avg_discount_rate,
    AVG(o.order_item_profit_ratio) AS avg_profit_ratio,
    SUM(o.order_item_total) AS total_profit,
	SUM(o.order_profit_per_order) AS t_order_profit_per_order,
	SUM(o.sales) AS total_sales
FROM orders o
JOIN orders_dim od ON o.order_id = od.order_id
JOIN customers_dim c ON o.customer_id = c.customer_id  -- Relacionamos con la dimensión de clientes
JOIN products_dim p ON o.product_name = p.product_name  -- 🔹 Mapeamos por nombre del producto
JOIN time_dim t1 ON date_trunc('hour', o.order_date) = t1.date_value
JOIN time_dim t2 ON date_trunc('hour', o.shipping_date) = t2.date_value
GROUP BY od.order_id, c.customer_id, p.product_id, t1.time_dim_id, t2.time_dim_id
ORDER BY od.order_id;

