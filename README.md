<div style="display: flex; justify-content: center;">
    <h1>SupplyRisk <span style="color:rgb(96, 180, 255);">AI</span></h1>
</div>
<h4>¡Somos el Equipo <i style="color:rgb(255, 189, 69);">S21-08-N-Data</i> y les presentamos nuestro MVP!</h4>
<h2 style="text-align: center;">Predictor de riesgo para envíos tardíos en cadenas de suministro</h2>

<hr></hr>

#### Integrantes

<table style="border-collapse: collapse; width: 600px; margin: auto; text-align: center; background: white; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); border-radius: 10px; table-layout: fixed;">
    <tr style="background-color: #4CAF50; color: white;">
        <th style="padding: 12px; border: 1px solid #ddd; width: 25%;">Nombre</th>
        <th style="padding: 12px; border: 1px solid #ddd; width: 25%;">Rol</th>
        <th style="padding: 12px; border: 1px solid #ddd; width: 25%;">LinkedIn</th>
        <th style="padding: 12px; border: 1px solid #ddd; width: 25%;">GitHub</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;">Juan Mora</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Ingeniero de datos</td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://www.linkedin.com/in/jsebastianm/" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">LinkedIn</a></td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://github.com/JSEB99" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">GitHub</a></td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;">Livan Gonzalez</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Analista de datos</td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://www.linkedin.com/in/red-smile-/" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">LinkedIn</a></td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://github.com/R3dsm1le" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">GitHub</a></td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;">Juan Guerrero</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Científico de datos</td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://www.linkedin.com/in/juanvicente0104/" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">LinkedIn</a></td>
        <td style="padding: 12px; border: 1px solid #ddd;"><a href="https://github.com/juanvicente0104" target="_blank" style="text-decoration: none; color: #007bff; font-weight: bold;">GitHub</a></td>
    </tr>
</table>


<hr></hr>

#### Descripción y objetivo del proyecto

**Situación inicial**

En un mundo donde las cadenas de suministro globales enfrentan desafíos constantes, desde problemas logísticos hasta condiciones climáticas adversas, la eficiencia en la entrega de pedidos se vuelve un factor crítico para empresas y consumidores.  

**SupplyRisk AI** surge como una solución innovadora para abordar este problema. Utilizando técnicas avanzadas de análisis de datos y machine learning, este proyecto tiene como objetivo identificar patrones en los retrasos de envíos internacionales y predecir con precisión el riesgo de demoras.  

El análisis se basa en un dataset con información detallada sobre órdenes realizadas por vendedores en Estados Unidos con destino a múltiples países. A partir de estos datos, *tenemos los siguientes objetivos:*

1️⃣ **Clasificación de envíos tardíos:** Identificar si un pedido será entregado a tiempo o sufrirá un retraso.

2️⃣ **Análisis de factores de riesgo:** Determinar las variables que más influyen en los retrasos (ubicación del proveedor, tipo de producto, temporada, etc.).

3️⃣ **Optimización y alertas:** Proporcionar información útil para optimizar la logística y generar alertas tempranas de riesgo de retraso.

Con estas predicciones, empresas y clientes podrán tomar decisiones informadas, optimizar sus procesos logísticos y reducir los costos asociados a las demoras.

> [!NOTE]
> Fuente del dataset: [Kaggle dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

<hr></hr>

#### Diccionario de datos

Aquí tienes el diccionario de datos basado en la estructura proporcionada:  

### 📌 **Diccionario de Datos - SupplyRisk AI**  

| **Nombre del Campo**                  | **Tipo de Dato** | **Descripción** |
|----------------------------------------|-----------------|----------------|
| `fact_id`                              | INT             | Identificador único de la transacción en la tabla de hechos. |
| `order_id`                             | INT             | Identificador único del pedido. |
| `customer_id`                          | INT             | Identificador único del cliente. |
| `product_id`                           | INT             | Identificador único del producto. |
| `time_order_dim_id`                    | INT             | Identificador de la fecha en la que se realizó el pedido. |
| `time_shipping_dim_id`                 | INT             | Identificador de la fecha en la que se realizó el envío. |
| `order_item_quantity`                  | INT             | Cantidad de unidades del producto en la orden. |
| `order_item_discount`                  | FLOAT           | Descuento total aplicado al producto en la orden. |
| `order_item_discount_rate`             | FLOAT           | Porcentaje de descuento aplicado al producto. |
| `order_item_profit_ratio`              | FLOAT           | Margen de ganancia del producto en la orden. |
| `order_item_total`                     | FLOAT           | Total de la orden antes de descuentos e impuestos. |
| `order_profit_per_order`               | FLOAT           | Ganancia neta generada por la orden. |
| `sales`                                | FLOAT           | Valor total de la venta. |
| `order_status`                         | VARCHAR         | Estado actual del pedido (ej. `CLOSED`, `PENDING_PAYMENT`). |
| `order_region`                         | VARCHAR         | Región geográfica del pedido. |
| `order_country`                        | VARCHAR         | País de destino del pedido. |
| `order_state`                          | VARCHAR         | Estado o provincia del pedido. |
| `order_city`                           | VARCHAR         | Ciudad de destino del pedido. |
| `order_market`                         | VARCHAR         | Mercado o continente del pedido (ej. `LATAM`). |
| `order_shipping_mode`                  | VARCHAR         | Método de envío seleccionado (ej. `Standard Class`). |
| `order_delivery_status`                | VARCHAR         | Estado del envío (ej. `Advance shipping`). |
| `order_days_for_shipping_real`         | INT             | Número real de días que tardó el pedido en ser entregado. |
| `order_days_for_shipment_scheduled`    | INT             | Número de días programados para el envío del pedido. |
| `order_payment_type`                   | VARCHAR         | Método de pago utilizado en la transacción (ej. `CASH`, `PAYMENT`). |
| `order_late_delivery_risk`             | BOOLEAN         | Indica si el pedido tiene riesgo de entrega tardía (`1`= Sí, `0`= No). |
| `date_value`                           | DATETIME        | Fecha y hora de la transacción. |
| `date_year`                            | INT             | Año de la transacción. |
| `date_month`                           | INT             | Mes de la transacción. |
| `date_day`                             | INT             | Día del mes en que ocurrió la transacción. |
| `date_weekday`                         | INT             | Día de la semana en formato numérico (ej. `0=Domingo`, `6=Sábado`). |
| `date_hour`                            | INT             | Hora en la que se registró la transacción. |
| `customer_first_name`                  | VARCHAR         | Nombre del cliente. |
| `customer_last_name`                   | VARCHAR         | Apellido del cliente. |
| `customer_type`                        | VARCHAR         | Tipo de cliente (ej. `Consumer`). |
| `customer_store_state`                 | VARCHAR         | Estado donde se ubica la tienda del cliente. |
| `customer_store_city`                  | VARCHAR         | Ciudad donde se ubica la tienda del cliente. |
| `customer_store_street`                | VARCHAR         | Dirección de la tienda del cliente. |
| `customer_store_zipcode`               | VARCHAR         | Código postal de la tienda del cliente. |
| `customer_store_latitude`              | FLOAT           | Latitud de la tienda del cliente. |
| `customer_store_longitude`             | FLOAT           | Longitud de la tienda del cliente. |
| `product_name`                         | VARCHAR         | Nombre del producto adquirido. |
| `product_price`                        | FLOAT           | Precio del producto. |
| `category_id`                          | INT             | Identificador de la categoría del producto. |
| `department_id`                        | INT             | Identificador del departamento del producto. |
| `category_name`                        | VARCHAR         | Nombre de la categoría del producto (ej. `Men's Footwear`). |
| `department_name`                      | VARCHAR         | Nombre del departamento del producto (ej. `Apparel`). |

<hr></hr>

#### Análisis y hallazgos clave

Para resolver el problema, realizamos un **análisis descriptivo y exploratorio** de los datos, centrándonos en identificar patrones y tendencias que pudieran indicar fraudes. Estos fueron los insights más relevantes:

1️⃣ **Análisis de retrasos en los envíos** 

- Retraso promedio de **2 días** por países.
- Existe una clase mayoritaria `Standard Class` que se dispone de 4 días programados, donde representa el **59.68 %**
- Entre cancelados y sospechosos de fraude se mantienen durante los años, estos representan una clase de posibles demoras.
- Por region y mercado, mantienen los días reales entre 3 y 4 días
y los programados cercanos a 3, un 2.9 aproximadamente.
- **54.82 %** representan las ordenes que presentaron demoras, que son **87194**
- De `16001` clientes que presentaron demoras, un **35.21%** no volvieron a comprar despues de presentar una demora.

2️⃣ **Optimización del proceso logístico**

- Promedio de entrega por productos es **0.57 días**
- Promedio de demora en ordenes con retraso es **0.8 días**
- Existen 4 productos que estan por encima de **0.8 días** de retraso, siendo un producto **SOLE E25 Elliptical** tiene un promedio de **1 día**, haciendo un margen importante para mantener un promedio tan alto de demora.
- **52 productos** tienen un promedio de demora por encima de la media general de `0.57 días`

3️⃣ **Impacto en la rentabilidad**

- No se ve una diferencia notable entre demoras y no demoras respecto con las ganancias.
- No se ve una diferencia notable entre demoras con respecto productos con descuento y sin descuento.

<hr></hr>

#### Solución predictiva

La implementación del modelo de predicción de retrasos en envíos dentro de la cadena de suministro ha permitido identificar patrones clave en los factores que influyen en las demoras. A través del uso de técnicas de machine learning, se logró desarrollar un modelo con una precisión significativa para anticipar si un pedido llegará tarde o no.

> [!CAUTION]
> El modelo esta establecido según unos criterios y datos recomendados, estos se revelan en el formulario, por lo cual se sugiere seguirlos para un correcto funcionamiento

<hr></hr>

#### Tecnologías

<img align="left" alt="Python" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"/>
<img align="left" alt="Pandas" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg"/>
<img align="left" alt="Numpy" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-plain.svg"/>
<img align="left" alt="Scikit-learn" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg"/>
<img align="left" alt="SQLAlchemy" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlalchemy/sqlalchemy-original-wordmark.svg"/>
<img align="left" alt="PostgreSQL" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg"/>
<img align="left" alt="Supabase" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/supabase/supabase-original.svg"/>
<img align="left" alt="Jupyter" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/jupyter/jupyter-original.svg"/>
<img align="left" alt="Streamlit" width="50px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-plain-wordmark.svg"/>

<br clear="left">

<hr></hr>

#### Instrucciones

El proyecto esta estructurado en directorios con las tareas especificas, todo esto para evitar conflictos entre las tareas:
- **app**: interfaz de usuario del proyecto, interactua internamente con el API y Base de Datos
- **sql**: contiene el esquema de la base de datos, de manera local estaría presente en la creación y almacenamiento de la información
- **notebooks**: desarrollo del análisis para el desarrollo del modelo predictivo
- **src**: contiene base de datos, modelos y utilidades
  - models: empaquetados para ejecución del modelo predictivo
  - db: base de datos y queries utilizados
  - utils: scripts de python con utilidades usadas.
- **data**: datos `*.csv` procesados, en crudo y externos.
  
1️⃣ **APP**
- Se debe crear un ambiente dentro del directorio `python -m venv .venv`
- Instalar las librerías del archivo requirements `pip install -r requirements.txt`

> [!WARNING]
> En el proyecto se uso una base de datos desplegada, donde las credenciales se guardan en un archivo **secrets.toml** este se debe ubicar en el mismo directorio **.streamlit**, en este caso deberías usar las credenciales de tu base de datos.

- Ejecución del proyecto, hacerlo desde la raíz del proyecto `streamlit run app/0_home.py`

2️⃣ **SRC/DB**

- Se deben aplicar a los datos del dataset las funciones, procesos y ejecuciones para limpiar y transformar los datos.
- Luego crear el modelo **OLAP** y cargar los datos del dataset limpio a este modelo

3️⃣ **SRC/UTILS**

- Se debe crear un ambiente dentro del directorio `python -m venv .venv`
- Instalar las librerías del archivo requirements `pip install -r requirements.txt`
- Aqui ya podras ejecutar cada script que desees probar

