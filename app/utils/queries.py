# 1. Análisis de retrasos en los envíos
# - ¿Qué países tienen los tiempos de entrega más largos?
TOP_10_DELAY_COUNTRIES = """
SELECT od.order_country AS "Pais",
       ROUND(AVG(od.order_days_for_shipping_real - od.order_days_for_shipment_scheduled),2) AS "Demora Promedio"
FROM order_facts of JOIN orders_dim od 
  ON of.order_id = od.order_id 
GROUP BY od.order_country
ORDER BY "Demora Promedio" DESC
LIMIT 10;
"""
# - ¿Cómo varía el tiempo de envío real vs. programado según la región o el mercado?
REGION_AVG_TIME = """
SELECT
	od.order_region,
  ROUND(AVG(od.order_days_for_shipping_real),1) AS "Envio Real", 
  ROUND(AVG(od.order_days_for_shipment_scheduled),1) AS "Envio programado"
FROM orders_dim of JOIN orders_dim od 
  ON of.order_id = od.order_id 
GROUP BY od.order_region,od.order_market
ORDER BY od.order_market, "Envio Real" DESC;
"""
MARKET_AVG_TIME = """
SELECT
	od.order_market,
  ROUND(AVG(od.order_days_for_shipping_real),1) AS "Envio Real", 
  ROUND(AVG(od.order_days_for_shipment_scheduled),1) AS "Envio programado"
FROM orders_dim of JOIN orders_dim od 
  ON of.order_id = od.order_id 
GROUP BY od.order_market
ORDER BY "Envio Real" DESC;
"""
# - ¿Cuántos pedidos llegan tarde y cuál es el porcentaje sobre el total?
LATE_DELIVERY_PCT = """
SELECT
  CASE
    WHEN od.order_late_delivery_risk=1 THEN 'Demorado'
    ELSE 'No demorado'
  END AS "Estado",
  COUNT(order_late_delivery_risk) AS "Total",
  ROUND((COUNT(od.order_late_delivery_risk) * 100.0) / SUM(COUNT(*)) OVER (),2) AS "Porcentaje"
FROM order_facts of JOIN orders_dim od 
  ON of.order_id = od.order_id 
GROUP BY od.order_late_delivery_risk;
"""
# - ¿Los clientes que experimentan retrasos en sus envíos son más propensos a no volver a comprar?
DELAY_CUSTOMER_ORDERS = """
WITH 
clientes_con_retraso AS (
  SELECT
    cd.customer_id,
    td.date_value as "scheduled",
    ROW_NUMBER() OVER(PARTITION BY cd.customer_id ORDER BY td.date_value) AS "pos",
    'demorado' AS "demorado"
  FROM order_facts of JOIN customers_dim cd
    ON of.customer_id = cd.customer_id JOIN orders_dim od  
      ON of.order_id = od.order_id JOIN time_dim td 
        ON of.time_order_dim_id = td.time_dim_id 
  WHERE od.order_delivery_status = 'Late delivery'
),
pedidos_antes_del_retraso AS (
  SELECT
    ccr.customer_id,
    COUNT(CASE WHEN td.date_value < ccr.scheduled THEN 1 END) AS "pedidos_antes",
    COUNT(CASE WHEN td.date_value > ccr.scheduled THEN 1 END) AS "pedidos_despues"
  FROM order_facts of JOIN time_dim td 
      ON of.time_order_dim_id = td.time_dim_id JOIN clientes_con_retraso ccr 
        ON of.customer_id = ccr.customer_id
  GROUP BY ccr.customer_id
  ORDER BY pedidos_antes DESC
),
pedidos_clientes_retraso AS (
  SELECT
    ccr.customer_id,
    COUNT(ccr.customer_id) AS pedidos_por_cliente
  FROM order_facts of JOIN clientes_con_retraso ccr 
    ON of.customer_id = ccr.customer_id
  GROUP BY ccr.customer_id
),
medidas_retrasos AS (
  SELECT
    AVG(pedidos_por_cliente),
    MAX(pedidos_por_cliente),
    MIN(pedidos_por_cliente),
    COUNT(customer_id) AS Total_clientes,
    PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY pedidos_por_cliente) AS mediana
  FROM pedidos_clientes_retraso
)
SELECT
  COUNT(CASE WHEN pedidos_despues = 0 THEN 1 END) AS "no_buy",
  COUNT(CASE WHEN pedidos_despues < (SELECT mediana FROM medidas_retrasos)-6
    or pedidos_despues < (SELECT mediana FROM medidas_retrasos)+6 THEN 1 END) AS "around_median",
  COUNT(CASE WHEN pedidos_despues > 0 THEN 1 END) AS "continue_buy",
  COUNT(1) AS "total",
  ROUND(100.0 * COUNT(CASE WHEN pedidos_despues = 0 THEN 1 END) / COUNT(*), 2) AS "No continuan",
  ROUND(100.0 * COUNT(CASE WHEN pedidos_despues > 0 THEN 1 END) / COUNT(*), 2) AS "Si continuan"
FROM pedidos_antes_del_retraso;
"""
DELAY_CUSTOMER_STATS = """
WITH 
clientes_con_retraso AS (
  SELECT
    cd.customer_id,
    td.date_value as "scheduled",
    ROW_NUMBER() OVER(PARTITION BY cd.customer_id ORDER BY td.date_value) AS "pos",
    'demorado' AS "demorado"
  FROM order_facts of JOIN customers_dim cd
    ON of.customer_id = cd.customer_id JOIN orders_dim od  
      ON of.order_id = od.order_id JOIN time_dim td 
        ON of.time_order_dim_id = td.time_dim_id 
  WHERE od.order_delivery_status = 'Late delivery'
),
pedidos_antes_del_retraso AS (
  SELECT
    ccr.customer_id,
    COUNT(CASE WHEN td.date_value < ccr.scheduled THEN 1 END) AS "pedidos_antes",
    COUNT(CASE WHEN td.date_value > ccr.scheduled THEN 1 END) AS "pedidos_despues"
  FROM order_facts of JOIN time_dim td 
      ON of.time_order_dim_id = td.time_dim_id JOIN clientes_con_retraso ccr 
        ON of.customer_id = ccr.customer_id
  GROUP BY ccr.customer_id
  ORDER BY pedidos_antes DESC
),
pedidos_clientes_retraso AS (
  SELECT
    ccr.customer_id,
    COUNT(ccr.customer_id) AS pedidos_por_cliente
  FROM order_facts of JOIN clientes_con_retraso ccr 
    ON of.customer_id = ccr.customer_id
  GROUP BY ccr.customer_id
),
medidas_retrasos AS (
  SELECT
    ROUND(AVG(pedidos_por_cliente),2) AS "avg",
    MAX(pedidos_por_cliente),
    MIN(pedidos_por_cliente),
    COUNT(customer_id) AS Total_clientes,
    PERCENTILE_CONT(.5) WITHIN GROUP (ORDER BY pedidos_por_cliente) AS mediana
  FROM pedidos_clientes_retraso
)
SELECT * FROM medidas_retrasos;
"""
# ¿Qué variables tienen mayor peso para determinar el tiempo máximo de entrega?
VARIABLES_IMPACT = """
with ordenes as (
select order_days_for_shipment_scheduled , order_late_delivery_risk from order_facts b inner join
orders_dim a
on a.order_id = b.order_id
)
select distinct order_days_for_shipment_scheduled , count(order_late_delivery_risk) as cuenta from ordenes
group by order_days_for_shipment_scheduled
"""
ESTADO_ORDEN = """
with ordenes_con_fechas as (
select a.date_year , b.order_id from time_dim a inner join order_facts b
on a.time_dim_id = b.time_shipping_dim_id
)
select a.date_year, b.order_status AS "Estado de orden", COUNT(a.date_year) from ordenes_con_fechas a inner join orders_dim b
on a.order_id = b.order_id
GROUP BY b.order_status,a.date_year
ORDER BY a.date_year,b.order_status;
"""
# 2. Optimización del proceso logístico
# ¿Cómo impacta el tipo de producto en los tiempos de entrega?
PRODUCT_IMPACT = """
WITH 
avg_delay_tb AS (
  SELECT
    ROUND(AVG(o.order_days_for_shipping_real - o.order_days_for_shipment_scheduled),2) AS avg_delay
  FROM order_facts f
  JOIN orders_dim o ON f.order_id = o.order_id
),
avg_per_product_tb AS (
  SELECT p.product_name, 
    ROUND(AVG(o.order_days_for_shipping_real - o.order_days_for_shipment_scheduled),2) AS avg_delay
  FROM order_facts f
    JOIN products_dim p ON f.product_id = p.product_id
    JOIN orders_dim o ON f.order_id = o.order_id
  GROUP BY p.product_name
  ORDER BY avg_delay DESC
)
SELECT
  *
FROM avg_per_product_tb
LIMIT 10;
"""
TOTAL_PRODUCT = """
WITH 
avg_delay_tb AS (
  SELECT
    ROUND(AVG(o.order_days_for_shipping_real - o.order_days_for_shipment_scheduled),2) AS avg_delay
  FROM order_facts f
  JOIN orders_dim o ON f.order_id = o.order_id
),
avg_per_product_tb AS (
  SELECT p.product_name, 
    ROUND(AVG(o.order_days_for_shipping_real - o.order_days_for_shipment_scheduled),2) AS avg_delay
  FROM order_facts f
    JOIN products_dim p ON f.product_id = p.product_id
    JOIN orders_dim o ON f.order_id = o.order_id
  GROUP BY p.product_name
  ORDER BY avg_delay DESC
),
total_productos_over_delay AS (
  SELECT
    COUNT(1) AS "Total"
  FROM avg_per_product_tb
  WHERE
    avg_delay > (SELECT avg_delay FROM avg_delay_tb)
)
SELECT * FROM total_productos_over_delay;
"""
# 3. Impacto en la rentabilidad
# ¿Cómo afecta el retraso de un pedido a la rentabilidad de la empresa?
RENTABILIDAD = """
SELECT 
    CASE WHEN o.order_days_for_shipping_real > o.order_days_for_shipment_scheduled THEN 'Delayed' ELSE 'On Time' END AS delivery_status,
    ROUND(AVG(f.order_profit_per_order),2) AS avg_profit
FROM order_facts f
JOIN orders_dim o ON f.order_id = o.order_id
GROUP BY delivery_status;
"""
# ¿Los pedidos con descuentos o promociones tienden a experimentar más retrasos?
DISCOUNTS = """
SELECT 
    CASE WHEN order_item_discount > 0 THEN 'Discounted' ELSE 'No Discount' END AS discount_status,
    ROUND(AVG(order_days_for_shipping_real - order_days_for_shipment_scheduled),4) AS avg_delay
FROM order_facts of JOIN orders_dim od ON of.order_id = od.order_id
GROUP BY discount_status;
"""
