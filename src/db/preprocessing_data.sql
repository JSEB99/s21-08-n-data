-- Formato de fecha
SET datestyle = 'ISO, MDY';
-- Crear tabla raw
CREATE TABLE orders (
    trans_type VARCHAR(20),
    days_for_shipping_real SMALLINT,
    days_for_shipment_scheduled SMALLINT,
    benefit_per_order NUMERIC(10,2),
    sales_per_customer NUMERIC(10,2),
    delivery_status VARCHAR(30),
    late_delivery_risk SMALLINT,
    category_id SMALLINT,
    category_name VARCHAR(30),
    customer_city VARCHAR(30),
    customer_country VARCHAR(30),
    customer_email VARCHAR(100),
    customer_fname VARCHAR(30),
    customer_id SMALLINT,
    customer_lname VARCHAR(30),
    customer_password VARCHAR(30),
    customer_segment VARCHAR(50),
    customer_state VARCHAR(30),
    customer_street VARCHAR(255),
    customer_zipcode VARCHAR(10),
    department_id SMALLINT,
    department_name VARCHAR(30),
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    market VARCHAR(20),
    order_city VARCHAR(40),
    order_country VARCHAR(40),
    order_customer_id SMALLINT,
    order_date TIMESTAMP WITH TIME ZONE,
    order_id INT,
    order_item_cardprod_id SMALLINT,
    order_item_discount NUMERIC(10,5),
    order_item_discount_rate NUMERIC(5,4),
    order_item_id INT,
    order_item_product_price NUMERIC(10,2),
    order_item_profit_ratio NUMERIC(5,4),
    order_item_quantity SMALLINT,
    sales NUMERIC(10,2),
    order_item_total NUMERIC(10,2),
    order_profit_per_order NUMERIC(10,2),
    order_region VARCHAR(30),
    order_state VARCHAR(40),
    order_status VARCHAR(30),
    order_zipcode VARCHAR(10),
    product_card_id SMALLINT,
    product_category_id SMALLINT,
    product_description TEXT,
    product_image TEXT,
    product_name VARCHAR(255),
    product_price NUMERIC(10,2),
    product_status BOOLEAN,
    shipping_date TIMESTAMP WITH TIME ZONE,
    shipping_mode VARCHAR(50)
);
-- Cargar datos
COPY orders
FROM 'D:\no-country\data\DataCoSupplyChainDataset.csv'
WITH (FORMAT CSV, HEADER, ENCODING 'LATIN1');
-- Limpieza de preprocesamiento
-- Eliminar columnas
CREATE OR REPLACE PROCEDURE del_columns()
LANGUAGE plpgsql
AS
$$
BEGIN
    EXECUTE 'ALTER TABLE orders DROP COLUMN customer_email';
    EXECUTE 'ALTER TABLE orders DROP COLUMN customer_password';
    EXECUTE 'ALTER TABLE orders DROP COLUMN product_description';
    EXECUTE 'ALTER TABLE orders DROP COLUMN product_image';
    EXECUTE 'ALTER TABLE orders DROP COLUMN order_zipcode';
	EXECUTE 'ALTER TABLE orders DROP COLUMN customer_country';
	EXECUTE 'ALTER TABLE orders ADD COLUMN customer_order_date TIMESTAMP':
END;
$$;
-- Eliminar nulos
CREATE OR REPLACE PROCEDURE del_nul_cols(col TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
	EXECUTE format('DELETE FROM orders WHERE %I IS NULL', col);
END;
$$;
-- Normalización
-- Concatenación de Zipcodes
-- Customer_zipcode
CREATE OR REPLACE PROCEDURE update_cols()
LANGUAGE plpgsql
AS $$
BEGIN
UPDATE orders
SET customer_zipcode = LPAD(customer_zipcode,5,'0')
WHERE LENGTH(customer_zipcode)<5;
END;
$$;
-- Actualizar New York City a New York en Ciudad
UPDATE orders
SET order_city = 'New York'
WHERE order_city = 'New York City';
-- Actualizar customer_state
CREATE OR REPLACE FUNCTION state_name(state_code VARCHAR(2))
RETURNS TEXT AS
$$
	BEGIN
		RETURN CASE
			WHEN state_code = 'CA' THEN 'California'
	        WHEN state_code = 'OR' THEN 'Oregon'
	        WHEN state_code = 'ND' THEN 'North Dakota'
	        WHEN state_code = 'TX' THEN 'Texas'
	        WHEN state_code = 'PR' THEN 'Puerto Rico'
	        WHEN state_code = 'NV' THEN 'Nevada'
	        WHEN state_code = 'KY' THEN 'Kentucky'
	        WHEN state_code = 'OH' THEN 'Ohio'
	        WHEN state_code = 'NY' THEN 'New York'
	        WHEN state_code = 'HI' THEN 'Hawaii'
	        WHEN state_code = 'NM' THEN 'New Mexico'
	        WHEN state_code = 'IN' THEN 'Indiana'
	        WHEN state_code = 'DC' THEN 'District of Columbia'
	        WHEN state_code = 'WV' THEN 'West Virginia'
	        WHEN state_code = 'MO' THEN 'Missouri'
	        WHEN state_code = 'FL' THEN 'Florida'
	        WHEN state_code = 'AR' THEN 'Arkansas'
	        WHEN state_code = 'WI' THEN 'Wisconsin'
	        WHEN state_code = 'NC' THEN 'North Carolina'
	        WHEN state_code = 'CT' THEN 'Connecticut'
	        WHEN state_code = 'OK' THEN 'Oklahoma'
	        WHEN state_code = 'RI' THEN 'Rhode Island'
	        WHEN state_code = 'ID' THEN 'Idaho'
	        WHEN state_code = 'GA' THEN 'Georgia'
	        WHEN state_code = 'MN' THEN 'Minnesota'
	        WHEN state_code = 'PA' THEN 'Pennsylvania'
	        WHEN state_code = 'MD' THEN 'Maryland'
	        WHEN state_code = 'LA' THEN 'Louisiana'
	        WHEN state_code = 'MT' THEN 'Montana'
	        WHEN state_code = 'IL' THEN 'Illinois'
	        WHEN state_code = 'TN' THEN 'Tennessee'
	        WHEN state_code = 'WA' THEN 'Washington'
	        WHEN state_code = 'MI' THEN 'Michigan'
	        WHEN state_code = 'NJ' THEN 'New Jersey'
	        WHEN state_code = 'MA' THEN 'Massachusetts'
	        WHEN state_code = 'AL' THEN 'Alabama'
	        WHEN state_code = 'IA' THEN 'Iowa'
	        WHEN state_code = 'UT' THEN 'Utah'
	        WHEN state_code = 'CO' THEN 'Colorado'
	        WHEN state_code = 'SC' THEN 'South Carolina'
	        WHEN state_code = 'VA' THEN 'Virginia'
	        WHEN state_code = 'DE' THEN 'Delaware'
	        WHEN state_code = 'AZ' THEN 'Arizona'
	        WHEN state_code = 'KS' THEN 'Kansas'
	        ELSE state_code  -- Si el código no está en la lista, se devuelve tal cual
			END;
	END;
$$;
LANGUAGE plpgsql;
-- ACTUALIZACIÓN CUSTOMER_STATE
UPDATE orders
SET customer_state = state_name(customer_state)
END;

-- ORDER CITY, ORDER COUNTRY
-- ACTUALIZAR PAISES A INGLES
UPDATE orders
SET order_country = CASE 
    WHEN order_country = 'Afganistán' THEN 'Afghanistan'
    WHEN order_country = 'Albania' THEN 'Albania'
    WHEN order_country = 'Alemania' THEN 'Germany'
    WHEN order_country = 'Angola' THEN 'Angola'
    WHEN order_country = 'Arabia Saudí' THEN 'Saudi Arabia'
    WHEN order_country = 'Argelia' THEN 'Algeria'
    WHEN order_country = 'Argentina' THEN 'Argentina'
    WHEN order_country = 'Armenia' THEN 'Armenia'
    WHEN order_country = 'Australia' THEN 'Australia'
    WHEN order_country = 'Austria' THEN 'Austria'
    WHEN order_country = 'Azerbaiyán' THEN 'Azerbaijan'
    WHEN order_country = 'Bangladés' THEN 'Bangladesh'
    WHEN order_country = 'Barbados' THEN 'Barbados'
    WHEN order_country = 'Baréin' THEN 'Bahrain'
    WHEN order_country = 'Bélgica' THEN 'Belgium'
    WHEN order_country = 'Belice' THEN 'Belize'
    WHEN order_country = 'Benín' THEN 'Benin'
    WHEN order_country = 'Bielorrusia' THEN 'Belarus'
    WHEN order_country = 'Bolivia' THEN 'Bolivia'
    WHEN order_country = 'Bosnia y Herzegovina' THEN 'Bosnia and Herzegovina'
    WHEN order_country = 'Botsuana' THEN 'Botswana'
    WHEN order_country = 'Brasil' THEN 'Brazil'
    WHEN order_country = 'Bulgaria' THEN 'Bulgaria'
    WHEN order_country = 'Burkina Faso' THEN 'Burkina Faso'
    WHEN order_country = 'Burundi' THEN 'Burundi'
    WHEN order_country = 'Bután' THEN 'Bhutan'
    WHEN order_country = 'Camboya' THEN 'Cambodia'
    WHEN order_country = 'Camerún' THEN 'Cameroon'
    WHEN order_country = 'Canada' THEN 'Canada'
    WHEN order_country = 'Chad' THEN 'Chad'
    WHEN order_country = 'Chile' THEN 'Chile'
    WHEN order_country = 'China' THEN 'China'
    WHEN order_country = 'Chipre' THEN 'Cyprus'
    WHEN order_country = 'Colombia' THEN 'Colombia'
    WHEN order_country = 'Corea del Sur' THEN 'South Korea'
    WHEN order_country = 'Costa de Marfil' THEN 'Ivory Coast'
    WHEN order_country = 'Costa Rica' THEN 'Costa Rica'
    WHEN order_country = 'Croacia' THEN 'Croatia'
    WHEN order_country = 'Cuba' THEN 'Cuba'
    WHEN order_country = 'Dinamarca' THEN 'Denmark'
    WHEN order_country = 'Ecuador' THEN 'Ecuador'
    WHEN order_country = 'Egipto' THEN 'Egypt'
    WHEN order_country = 'El Salvador' THEN 'El Salvador'
    WHEN order_country = 'Emiratos Árabes Unidos' THEN 'United Arab Emirates'
    WHEN order_country = 'Eritrea' THEN 'Eritrea'
    WHEN order_country = 'Eslovaquia' THEN 'Slovakia'
    WHEN order_country = 'Eslovenia' THEN 'Slovenia'
    WHEN order_country = 'España' THEN 'Spain'
    WHEN order_country = 'Estados Unidos' THEN 'United States'
    WHEN order_country = 'Estonia' THEN 'Estonia'
    WHEN order_country = 'Etiopía' THEN 'Ethiopia'
    WHEN order_country = 'Filipinas' THEN 'Philippines'
    WHEN order_country = 'Finlandia' THEN 'Finland'
    WHEN order_country = 'Francia' THEN 'France'
    WHEN order_country = 'Gabón' THEN 'Gabon'
    WHEN order_country = 'Georgia' THEN 'Georgia'
    WHEN order_country = 'Ghana' THEN 'Ghana'
    WHEN order_country = 'Grecia' THEN 'Greece'
    WHEN order_country = 'Guadalupe' THEN 'Guadeloupe'
    WHEN order_country = 'Guatemala' THEN 'Guatemala'
    WHEN order_country = 'Guayana Francesa' THEN 'French Guiana'
    WHEN order_country = 'Guinea' THEN 'Guinea'
    WHEN order_country = 'Guinea-Bissau' THEN 'Guinea-Bissau'
    WHEN order_country = 'Guinea Ecuatorial' THEN 'Equatorial Guinea'
    WHEN order_country = 'Guyana' THEN 'Guyana'
    WHEN order_country = 'Haití' THEN 'Haiti'
    WHEN order_country = 'Honduras' THEN 'Honduras'
    WHEN order_country = 'Hong Kong' THEN 'Hong Kong'
    WHEN order_country = 'Hungría' THEN 'Hungary'
    WHEN order_country = 'India' THEN 'India'
    WHEN order_country = 'Indonesia' THEN 'Indonesia'
    WHEN order_country = 'Irak' THEN 'Iraq'
    WHEN order_country = 'Irán' THEN 'Iran'
    WHEN order_country = 'Irlanda' THEN 'Ireland'
    WHEN order_country = 'Israel' THEN 'Israel'
    WHEN order_country = 'Italia' THEN 'Italy'
    WHEN order_country = 'Jamaica' THEN 'Jamaica'
    WHEN order_country = 'Japón' THEN 'Japan'
    WHEN order_country = 'Jordania' THEN 'Jordan'
    WHEN order_country = 'Kazajistán' THEN 'Kazakhstan'
    WHEN order_country = 'Kenia' THEN 'Kenya'
    WHEN order_country = 'Kirguistán' THEN 'Kyrgyzstan'
    WHEN order_country = 'Kuwait' THEN 'Kuwait'
    WHEN order_country = 'Laos' THEN 'Laos'
    WHEN order_country = 'Lesoto' THEN 'Lesotho'
    WHEN order_country = 'Líbano' THEN 'Lebanon'
    WHEN order_country = 'Liberia' THEN 'Liberia'
    WHEN order_country = 'Libia' THEN 'Libya'
    WHEN order_country = 'Lituania' THEN 'Lithuania'
    WHEN order_country = 'Luxemburgo' THEN 'Luxembourg'
    WHEN order_country = 'Macedonia' THEN 'North Macedonia'
    WHEN order_country = 'Madagascar' THEN 'Madagascar'
    WHEN order_country = 'Malasia' THEN 'Malaysia'
    WHEN order_country = 'Mali' THEN 'Mali'
    WHEN order_country = 'Marruecos' THEN 'Morocco'
    WHEN order_country = 'Martinica' THEN 'Martinique'
    WHEN order_country = 'Mauritania' THEN 'Mauritania'
    WHEN order_country = 'México' THEN 'Mexico'
    WHEN order_country = 'Moldavia' THEN 'Moldova'
    WHEN order_country = 'Mongolia' THEN 'Mongolia'
    WHEN order_country = 'Montenegro' THEN 'Montenegro'
    WHEN order_country = 'Mozambique' THEN 'Mozambique'
    WHEN order_country = 'Myanmar (Birmania)' THEN 'Myanmar'
    WHEN order_country = 'Namibia' THEN 'Namibia'
    WHEN order_country = 'Nepal' THEN 'Nepal'
    WHEN order_country = 'Nicaragua' THEN 'Nicaragua'
    WHEN order_country = 'Níger' THEN 'Niger'
    WHEN order_country = 'Nigeria' THEN 'Nigeria'
    WHEN order_country = 'Noruega' THEN 'Norway'
    WHEN order_country = 'Nueva Zelanda' THEN 'New Zealand'
    ELSE order_country -- Mantiene valores no traducidos
END;

-- ACTUALIZAR order_state A ingles, SOLO PARA USA
UPDATE orders
SET order_state = CASE 
    WHEN order_state = 'Alabama' THEN 'Alabama'
    WHEN order_state = 'Arizona' THEN 'Arizona'
    WHEN order_state = 'Arkansas' THEN 'Arkansas'
    WHEN order_state = 'California' THEN 'California'
    WHEN order_state = 'Carolina del Norte' THEN 'North Carolina'
    WHEN order_state = 'Carolina del Sur' THEN 'South Carolina'
    WHEN order_state = 'Colorado' THEN 'Colorado'
    WHEN order_state = 'Connecticut' THEN 'Connecticut'
    WHEN order_state = 'Dakota del Norte' THEN 'North Dakota'
    WHEN order_state = 'Dakota del Sur' THEN 'South Dakota'
    WHEN order_state = 'Delaware' THEN 'Delaware'
    WHEN order_state = 'Distrito de Columbia' THEN 'District of Columbia'
    WHEN order_state = 'Florida' THEN 'Florida'
    WHEN order_state = 'Georgia' THEN 'Georgia'
    WHEN order_state = 'Idaho' THEN 'Idaho'
    WHEN order_state = 'Illinois' THEN 'Illinois'
    WHEN order_state = 'Indiana' THEN 'Indiana'
    WHEN order_state = 'Iowa' THEN 'Iowa'
    WHEN order_state = 'Kansas' THEN 'Kansas'
    WHEN order_state = 'Kentucky' THEN 'Kentucky'
    WHEN order_state = 'Luisiana' THEN 'Louisiana'
    WHEN order_state = 'Maine' THEN 'Maine'
    WHEN order_state = 'Maryland' THEN 'Maryland'
    WHEN order_state = 'Massachusetts' THEN 'Massachusetts'
    WHEN order_state = 'Michigan' THEN 'Michigan'
    WHEN order_state = 'Minnesota' THEN 'Minnesota'
    WHEN order_state = 'Misisipi' THEN 'Mississippi'
    WHEN order_state = 'Misuri' THEN 'Missouri'
    WHEN order_state = 'Montana' THEN 'Montana'
    WHEN order_state = 'Nebraska' THEN 'Nebraska'
    WHEN order_state = 'Nevada' THEN 'Nevada'
    WHEN order_state = 'Nueva Jersey' THEN 'New Jersey'
    WHEN order_state = 'Nueva York' THEN 'New York'
    WHEN order_state = 'Nuevo Hampshire' THEN 'New Hampshire'
    WHEN order_state = 'Nuevo México' THEN 'New Mexico'
    WHEN order_state = 'Ohio' THEN 'Ohio'
    WHEN order_state = 'Oklahoma' THEN 'Oklahoma'
    WHEN order_state = 'Oregón' THEN 'Oregon'
    WHEN order_state = 'Pensilvania' THEN 'Pennsylvania'
    WHEN order_state = 'Rhode Island' THEN 'Rhode Island'
    WHEN order_state = 'Tennessee' THEN 'Tennessee'
    WHEN order_state = 'Texas' THEN 'Texas'
    WHEN order_state = 'Utah' THEN 'Utah'
    WHEN order_state = 'Vermont' THEN 'Vermont'
    WHEN order_state = 'Virginia' THEN 'Virginia'
    WHEN order_state = 'Virginia Occidental' THEN 'West Virginia'
    WHEN order_state = 'Washington' THEN 'Washington'
    WHEN order_state = 'Wisconsin' THEN 'Wisconsin'
    ELSE order_state -- Mantiene valores que no están en la lista
END
WHERE order_country = 'United States';

CREATE TEMP TABLE state_timezones (
    state TEXT PRIMARY KEY,
    timezone TEXT
);

INSERT INTO state_timezones (state, timezone) VALUES
('Alabama', 'America/Chicago'),
('Arizona', 'America/Phoenix'),
('Arkansas', 'America/Chicago'),
('California', 'America/Los_Angeles'),
('Colorado', 'America/Denver'),
('Connecticut', 'America/New_York'),
('Delaware', 'America/New_York'),
('District of Columbia', 'America/New_York'),
('Florida', 'America/New_York'),
('Georgia', 'America/New_York'),
('Hawaii', 'Pacific/Honolulu'),
('Idaho', 'America/Boise'),
('Illinois', 'America/Chicago'),
('Indiana', 'America/Indiana/Indianapolis'),
('Iowa', 'America/Chicago'),
('Kansas', 'America/Chicago'),
('Kentucky', 'America/New_York'),
('Louisiana', 'America/Chicago'),
('Maryland', 'America/New_York'),
('Massachusetts', 'America/New_York'),
('Michigan', 'America/Detroit'),
('Minnesota', 'America/Chicago'),
('Missouri', 'America/Chicago'),
('Montana', 'America/Denver'),
('Nevada', 'America/Los_Angeles'),
('New Jersey', 'America/New_York'),
('New Mexico', 'America/Denver'),
('New York', 'America/New_York'),
('North Carolina', 'America/New_York'),
('North Dakota', 'America/Chicago'),
('Ohio', 'America/New_York'),
('Oklahoma', 'America/Chicago'),
('Oregon', 'America/Los_Angeles'),
('Pennsylvania', 'America/New_York'),
('Puerto Rico', 'America/Puerto_Rico'),
('Rhode Island', 'America/New_York'),
('South Carolina', 'America/New_York'),
('Tennessee', 'America/Chicago'),
('Texas', 'America/Chicago'),
('Utah', 'America/Denver'),
('Virginia', 'America/New_York'),
('Washington', 'America/Los_Angeles'),
('West Virginia', 'America/New_York'),
('Wisconsin', 'America/Chicago');

UPDATE orders o
SET customer_order_date = order_date AT TIME ZONE stz.timezone
FROM state_timezones stz
WHERE o.customer_state = stz.state;
