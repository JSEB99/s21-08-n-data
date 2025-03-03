-- OLAP MODEL DESIGN
-- TIME DIMENSION
CREATE TABLE time_dim(
	time_dim_id SERIAL PRIMARY KEY,
	date_value TIMESTAMP UNIQUE,
	date_year SMALLINT,
	date_month SMALLINT,
	date_day SMALLINT,
	date_weekday SMALLINT,
	date_hour SMALLINT,
	-- FK
	CONSTRAINT check_date_value CHECK (date_value > '2013-12-31 23:00:00' AND date_value < '2022-02-06 22:00:00')
);
-- CUSTOMERS DIMENSION
CREATE TABLE customers_dim(
	customer_dim_id SERIAL PRIMARY KEY,
	customer_id SMALLINT UNIQUE,
	customer_first_name VARCHAR(30),
	customer_last_name VARCHAR(30),
	customer_type VARCHAR(50) NOT NULL,
	customer_store_state VARCHAR(30) NOT NULL,
	customer_store_city VARCHAR(30) NOT NULL,
	customer_store_street VARCHAR(255),
	customer_store_zipcode VARCHAR(10),
	customer_store_latitude NUMERIC(10,7) NOT NULL,
	customer_store_longitude NUMERIC(10,7) NOT NULL
);
-- PRODUCTS DIMENSION
-- CATEGORY_VALUES DEFINITIONS
CREATE TABLE category_values (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);
-- DEPARTMENT_VALUES DEFINITIONS
CREATE TABLE department_values (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);
-- PRODUCT DIMENSION TABLE
CREATE TABLE products_dim(
	product_dim_id SERIAL PRIMARY KEY,
    product_id INT UNIQUE,
    product_name VARCHAR(255),
    product_price NUMERIC(10,2),
    category_id INT NOT NULL,
    department_id INT NOT NULL,
	-- CONSTRAINTS
	CONSTRAINT check_product_price CHECK (product_price > 0),
	-- FK
	FOREIGN KEY (category_id) REFERENCES category_values(category_id),
    FOREIGN KEY (department_id) REFERENCES department_values(department_id)
);
-- ORDERS DIMENSION
CREATE TABLE orders_dim(
	order_dim_id SERIAL PRIMARY KEY,
	order_id INT UNIQUE,
	order_status VARCHAR(40) NOT NULL,
	order_region VARCHAR(30) NOT NULL,
	order_country VARCHAR(40) NOT NULL,
	order_state VARCHAR(40) NOT NULL,
	order_city VARCHAR(40),
	order_market VARCHAR(20),
	order_shipping_mode VARCHAR(40),
	order_delivery_status VARCHAR(30),
	order_days_for_shipping_real SMALLINT,
	order_days_for_shipment_scheduled SMALLINT,
	order_late_delivery_risk BOOLEAN,
	-- CONSTRAINTS
	order_payment_type VARCHAR(20) NOT NULL,
	CONSTRAINT check_order_days_for_shipping_real CHECK (order_days_for_shipping_real >= 0);
	CONSTRAINT check_order_days_for_shipment_scheduled CHECK (order_days_for_shipment_scheduled >= 0);
);
-- FACTS TABLE
-- ORDER FACTS TABLE
CREATE TABLE order_facts(
	fact_id SERIAL PRIMARY KEY,
	order_id INT,
	customer_id INT,
	product_id INT,
	time_order_dim_id INT,
	time_shipping_dim_id INT,
	-- Métricas
	order_item_quantity INT,
	order_item_discount NUMERIC(10,5),
	order_item_discount_rate NUMERIC(5,4),
	order_item_profit_ratio NUMERIC(5,4),
	order_item_total NUMERIC(10,2),
	order_profit_per_order NUMERIC(10,2),
	sales NUMERIC(10,2),
	-- FK
	FOREIGN KEY (order_id) REFERENCES orders_dim(order_id),
    FOREIGN KEY (customer_id) REFERENCES customers_dim(customer_id),
    FOREIGN KEY (product_id) REFERENCES products_dim(product_id),
    FOREIGN KEY (time_order_dim_id) REFERENCES time_dim(time_dim_id),
    FOREIGN KEY (time_shipping_dim_id) REFERENCES time_dim(time_dim_id),
	-- CONSTRAINTS
	CONSTRAINT check_sales CHECK (sales > 0),
	CONSTRAINT check_order_item_quantity CHECK (order_item_quantity > 0),
	CONSTRAINT check_order_item_discount CHECK (order_item_discount >= 0),
	CONSTRAINT check_order_item_total CHECK (order_item_total > 0)
);
