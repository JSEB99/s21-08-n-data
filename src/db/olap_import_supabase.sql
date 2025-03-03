-- CAMBIA CON TU RUTA
-- Exportando time_dim sin la PK (time_dim_id)
COPY (SELECT date_value, date_year, date_month, date_day, date_weekday, date_hour
      FROM time_dim)
TO 'D:\no-country\s21-08-n-data\data\processed\time_dim.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando orders_dim sin la PK (order_dim_id)
COPY (SELECT order_id, order_status, order_region, order_country, order_state, order_city, 
             order_market, order_shipping_mode, order_delivery_status, 
             order_days_for_shipping_real, order_days_for_shipment_scheduled, 
             order_late_delivery_risk, order_payment_type
      FROM orders_dim)
TO 'D:\no-country\s21-08-n-data\data\processed\orders_dim.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando customers_dim sin la PK (customer_dim_id)
COPY (SELECT customer_id, customer_first_name, customer_last_name, customer_type, 
             customer_store_state, customer_store_city, customer_store_street, 
             customer_store_zipcode, customer_store_latitude, customer_store_longitude
      FROM customers_dim)
TO 'D:\no-country\s21-08-n-data\data\processed\customers_dim.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando products_dim sin la PK (product_dim_id)
COPY (SELECT product_id, product_name, product_price, category_id, department_id
      FROM products_dim)
TO 'D:\no-country\s21-08-n-data\data\processed\products_dim.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando category_values sin la PK (category_id)
COPY (SELECT category_name
      FROM category_values)
TO 'D:\no-country\s21-08-n-data\data\processed\category_values.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando department_values sin la PK (department_id)
COPY (SELECT department_name
      FROM department_values)
TO 'D:\no-country\s21-08-n-data\data\processed\department_values.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- Exportando order_facts sin la PK (fact_id)
COPY (SELECT order_id, customer_id, product_id, time_order_dim_id, time_shipping_dim_id, 
             order_item_quantity, order_item_discount, order_item_discount_rate, 
             order_item_profit_ratio, order_item_total, order_profit_per_order, sales
      FROM order_facts)
TO 'D:\no-country\s21-08-n-data\data\processed\order_facts.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');

-- store procedure
CREATE OR REPLACE PROCEDURE load_data_from_csv()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Cargar datos en time_dim
    EXECUTE FORMAT(
        'COPY time_dim (date_value, date_year, date_month, date_day, date_weekday, date_hour)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/time_dim.csv'
    );

    -- Cargar datos en orders_dim
    EXECUTE FORMAT(
        'COPY orders_dim (order_id, order_status, order_region, order_country, order_state, order_city, 
                          order_market, order_shipping_mode, order_delivery_status, 
                          order_days_for_shipping_real, order_days_for_shipment_scheduled, 
                          order_late_delivery_risk, order_payment_type)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/orders_dim.csv'
    );

    -- Cargar datos en customers_dim
    EXECUTE FORMAT(
        'COPY customers_dim (customer_id, customer_first_name, customer_last_name, customer_type, 
                             customer_store_state, customer_store_city, customer_store_street, 
                             customer_store_zipcode, customer_store_latitude, customer_store_longitude)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/customers_dim.csv'
    );

    -- Cargar datos en products_dim
    EXECUTE FORMAT(
        'COPY products_dim (product_id, product_name, product_price, category_id, department_id)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/products_dim.csv'
    );

    -- Cargar datos en category_values
    EXECUTE FORMAT(
        'COPY category_values (category_name)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/category_values.csv'
    );

    -- Cargar datos en department_values
    EXECUTE FORMAT(
        'COPY department_values (department_name)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/department_values.csv'
    );

    -- Cargar datos en order_facts
    EXECUTE FORMAT(
        'COPY order_facts (order_id, customer_id, product_id, time_order_dim_id, time_shipping_dim_id, 
                           order_item_quantity, order_item_discount, order_item_discount_rate, 
                           order_item_profit_ratio, order_item_total, order_profit_per_order, sales)
         FROM %L WITH (FORMAT CSV, HEADER, DELIMITER ',')',
        'D:/no-country/s21-08-n-data/data/processed/order_facts.csv'
    );

END $$;

-- Para subirlo a supabase es con psql
psql -h HOST -p PUERTO -d postgres -U USUARIO
CALL load_data_from_csv();
