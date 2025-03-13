import streamlit as st
import utils.sidebar as sb

DESCRIPTION = """
Este proyecto tiene como objetivo **analizar y predecir el riesgo de retraso en los envíos** dentro de una cadena de suministro global. *Se trabaja con un dataset que contiene información sobre órdenes realizadas por vendedores en Estados Unidos*, con envíos a distintos puntos del mundo. Se busca **identificar patrones en los retrasos y estimar el tiempo adicional** que un pedido podría tardar en llegar si se considera tardío.

Para lograrlo, utilizamos `Python` para el procesamiento de datos, análisis exploratorio (*EDA*) y modelado predictivo, junto con `SQL` para la extracción, transformación y análisis de datos en un modelo de base de datos en estrella (*OLAP*).
"""

OBJETIVO = """
- **Clasificación de envíos tardíos:** Identificar si un pedido será entregado a tiempo o sufrirá un retraso.
- **Análisis de factores de riesgo:** Determinar las variables que más influyen en los retrasos (ubicación del proveedor, tipo de producto, temporada, etc.).
- **Optimización y alertas:** Proporcionar información útil para optimizar la logística y generar alertas tempranas de riesgo de retraso.
"""

st.set_page_config(
    page_title="SupplyRisk",
    layout="centered",
    page_icon="📦")

sb.show_sidebar()

st.markdown('<h1 style="background-color: rgb(96, 180, 255); color: white; padding: 5px; border-radius: 5px; text-align: center;">Predictor de riesgo para envíos tardíos en cadenas de suministro</h1>',
            unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.image("./assets/images/port.jpg")
st.subheader(":orange[Descripción]")
st.markdown(DESCRIPTION)
st.subheader(":orange[Objetivo]")
st.markdown(OBJETIVO)
