--Order Shipment and Delivery Risk
with ordenes as (
select order_days_for_shipment_scheduled , order_late_delivery_risk from orders_dim a inner join
order_facts b
on a.order_id = b.order_id
)
select distinct order_days_for_shipment_scheduled , count(order_late_delivery_risk) as cuenta from ordenes
group by order_days_for_shipment_scheduled 

--Orders with Shipping Dates
with ordenes_con_fechas as (
select a.date_year , b.order_id from time_dim a inner join order_facts b
on a.time_dim_id = b.time_shipping_dim_id
)
select a.date_year , b.order_status from ordenes_con_fechas a inner join orders_dim b
on a.order_id = b.order_id 

--Sample Order Facts Retrieval
with countries as (
select a.order_id , b.order_country , b.order_days_for_shipment_scheduled , b.order_days_for_shipping_real , 
(b.order_days_for_shipping_real - b.order_days_for_shipment_scheduled ) as substraccion_dias   from order_facts a inner join 
orders_dim b
on a.order_id = b.order_id 
)
select avg(substraccion_dias) as promedio , order_country from countries 
group by order_country
ORDER BY promedio desc
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY

--Order and Time Join
with fechas_ordenes as (
select a.order_id , a.time_order_dim_id , b.date_day , b.date_month from order_facts a inner join time_dim b
on a.time_order_dim_id   = b.time_dim_id 
),
quincenas as (
select a.order_delivery_status , b.date_day from orders_dim a
inner join fechas_ordenes b 
on a.order_id = b.order_id
where a.order_delivery_status = 'Late delivery'
and b.date_day = 15 
) ,

mensuales as (
select a.order_delivery_status , b.date_day from orders_dim a
inner join fechas_ordenes b 
on a.order_id = b.order_id
where a.order_delivery_status = 'Late delivery'
and b.date_day = 31
), 

primarios as (
select a.order_delivery_status , b.date_day from orders_dim a
inner join fechas_ordenes b 
on a.order_id = b.order_id
where a.order_delivery_status = 'Late delivery'
and b.date_day = 1
)
select count(*) as final_mes , 
(select count(*) as final_quincenas from quincenas) as final_quincenas  , (select count(*) as inicio_mes from primarios
) as inicio_mes from mensuales

--Fetch Sample Products
with llaves_categorizadas as (
select a.category_id , b.category_name , a.product_id from 
products_dim a inner join category_values b 
on a.category_id = b.category_id
) ,
 llaves_categorizadas_ordenes as(
 select a.order_id , b.category_name , b.product_id from order_facts a
 inner join llaves_categorizadas b 
 on a.product_id = b.product_id
)
select a.order_delivery_status, b.order_id , b.category_name , b.product_id from orders_dim a
inner join llaves_categorizadas_ordenes b 
on a.order_id = b.order_id 
where a.order_delivery_status = 'Late delivery'
