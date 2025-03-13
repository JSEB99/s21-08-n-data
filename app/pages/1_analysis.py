import streamlit as st
import utils.sidebar as sb
import utils.charts as chart
import utils.queries as query
import plotly.express as px

BAR_COLOR1 = "rgb(255, 189, 69)"
BAR_COLOR2 = "rgb(96, 180, 255)"
LINE_COLOR = "#F9FF95"
CARD_TITLE_COLOR1 = "rgb(255, 189, 69)"
CARD_BG_COLOR = "rgb(22, 84, 138)"


st.set_page_config(
    page_title="SupplyRisk - Analysis",
    layout="centered",
    page_icon="📊")

sb.show_sidebar()

st.markdown('<h1 style="background-color: rgb(96, 180, 255); color: white; padding: 5px; border-radius: 5px; text-align: center;">Análisis de los Datos</h1>',
            unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    st.markdown("## :orange[1. Análisis de retrasos en los envíos] 🛩️")
    st.markdown(
        "### ¿Qué países tienen los tiempos de entrega más largos?")

    top10_delay_countries = chart.get_cached_data(query.TOP_10_DELAY_COUNTRIES)
    max_delay = top10_delay_countries["Demora Promedio"].max()
    colors = [BAR_COLOR1 if delay ==
              max_delay else BAR_COLOR2 for delay in top10_delay_countries["Demora Promedio"]]
    fig_top10 = px.bar(top10_delay_countries, x="Pais", y="Demora Promedio", labels={
        'Pais': 'país', 'Demora Promedio': 'demora promedio (dias)'})
    fig_top10.update_traces(marker=dict(color=colors))
    avg_delay = top10_delay_countries["Demora Promedio"].mean()

    fig_top10.add_shape(
        type="line",
        # Extiende la línea a través de todas las barras
        x0=-0.5, x1=len(top10_delay_countries) - 0.5,
        y0=avg_delay, y1=avg_delay,  # Altura de la línea
        # Configuración de la línea
        line=dict(color=LINE_COLOR, width=2, dash="dash"),
    )

    fig_top10.add_annotation(
        x=len(top10_delay_countries)-2,
        y=avg_delay + 0.1,  # Un poco arriba de la línea
        text=f"Retraso promedio: {avg_delay:.2f} días",
        showarrow=False,  # No mostrar la flecha
        font=dict(size=12, color=LINE_COLOR)
    )

    st.plotly_chart(fig_top10)

    st.markdown(
        '### ¿Qué variables tienen mayor peso para determinar el tiempo máximo de entrega?')

    impact_variables = chart.get_cached_data(query.VARIABLES_IMPACT)

    max_variable = impact_variables["cuenta"].max()
    colors_var = [BAR_COLOR1 if variable ==
                  max_variable else BAR_COLOR2 for variable in impact_variables["cuenta"]]
    fig_variables = px.bar(impact_variables, x="order_days_for_shipment_scheduled", y="cuenta", labels={
        'order_days_for_shipment_scheduled': 'Días programados', 'cuenta': 'Cantidad de ordenes'})
    fig_variables.update_traces(marker=dict(color=colors_var))
    fig_variables.update_xaxes(type="category")
    avg_delay = impact_variables["cuenta"].mean()

    fig_variables.add_shape(
        type="line",
        # Extiende la línea a través de todas las barras
        x0=-0.5, x1=len(impact_variables) - 0.5,
        y0=avg_delay, y1=avg_delay,  # Altura de la línea
        # Configuración de la línea
        line=dict(color=LINE_COLOR, width=2, dash="dash"),
    )

    fig_variables.add_annotation(
        x=len(impact_variables)-2,
        y=avg_delay + 5000,  # Un poco arriba de la línea
        text=f"Orden promedio: {avg_delay:.1f}",
        showarrow=False,  # No mostrar la flecha
        font=dict(size=12, color=LINE_COLOR)
    )

    st.plotly_chart(fig_variables)

    order_status = chart.get_cached_data(query.ESTADO_ORDEN)
    st.bar_chart(order_status, x="date_year", y="count", x_label="Año",
                 y_label="Cantidad Ordenes", color="Estado de orden")

    st.markdown(
        "### ¿Cómo varía el tiempo de envío real vs. programado según la región o el mercado?")
    region, market = st.tabs(["Region", "Mercado"])

    with region:
        st.markdown("Envío real vs. programado según la **region**")
        region_time = chart.get_cached_data(query.REGION_AVG_TIME)
        st.bar_chart(region_time, x="order_region", y=["Envio programado", "Envio Real"],
                     color=[BAR_COLOR1, BAR_COLOR2], stack=False, x_label="Region", y_label=["Envío Real", "Envío Programado"])

    with market:
        st.markdown("Envío real vs. programado según el **mercado**")
        market_time = chart.get_cached_data(query.MARKET_AVG_TIME)
        st.bar_chart(market_time, x="order_market", y=["Envio programado", "Envio Real"],
                     color=[BAR_COLOR1, BAR_COLOR2], stack=False, x_label="Mercado", y_label=["Envío Real", "Envío Programado"])

    st.markdown(
        "### ¿Cuántos pedidos llegan tarde y cuál es el porcentaje sobre el total?")
    late_deliveries = chart.get_cached_data(query.LATE_DELIVERY_PCT)
    delay, delay_total, ontime, ontime_total = st.columns(4)

    with delay:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes Demoradas %",
                    BAR_COLOR2,
                    str(late_deliveries[late_deliveries["Estado"] == "Demorado"]["Porcentaje"].values[0])+" %")
    with delay_total:

        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes Demoradas",
                    BAR_COLOR2,
                    late_deliveries[late_deliveries["Estado"] == "Demorado"]["Total"].values[0])

    with ontime:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes No Demoradas %",
                    BAR_COLOR2,
                    str(late_deliveries[late_deliveries["Estado"] == "No demorado"]["Porcentaje"].values[0])+" %")

    with ontime_total:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes No Demoradas",
                    BAR_COLOR2,
                    late_deliveries[late_deliveries["Estado"] == "No demorado"]["Total"].values[0])

    st.markdown(
        "### ¿Los clientes que experimentan retrasos en sus envíos son más propensos a no volver a comprar?")

    delay_customer_stats = chart.get_cached_data(query.DELAY_CUSTOMER_STATS)
    delay_customer_orders = chart.get_cached_data(query.DELAY_CUSTOMER_ORDERS)[
        ["No continuan", "Si continuan"]].T.reset_index()
    delay_customer_orders.columns = ["category", "percentage"]
    col1, col2, col3 = st.columns(3)

    with col1:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Clientes con demoras", BAR_COLOR2,
                    delay_customer_stats["total_clientes"].values[0]
                    )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes (min)", BAR_COLOR2,
                    delay_customer_stats["min"].values[0]
                    )

    with col2:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes (avg)", BAR_COLOR2,
                    delay_customer_stats["avg"].values[0]
                    )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes (mediana)", BAR_COLOR2,
                    delay_customer_stats["mediana"].values[0]
                    )

    with col3:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ordenes (max)", BAR_COLOR2,
                    delay_customer_stats["max"].values[0]
                    )
        st.markdown("<br>", unsafe_allow_html=True)
        st.bar_chart(delay_customer_orders, x="category", y="percentage", x_label="% Continuan comprando",
                     y_label="Porcentaje %", color=BAR_COLOR1)

with st.container():
    st.markdown("## :orange[2. Optimización del proceso logístico] 📦")
    st.markdown(
        "### ¿Cómo impacta el tipo de producto en los tiempos de entrega?")
    top_products, total_products = st.columns([3, 1])

    top10_productos = chart.get_cached_data(query.PRODUCT_IMPACT)
    total_productos = chart.get_cached_data(query.TOTAL_PRODUCT)

    with top_products:
        max_delay_product = top10_productos["avg_delay"].max()
        color_products = [BAR_COLOR1 if delay ==
                          max_delay_product else BAR_COLOR2 for delay in top10_productos["avg_delay"]]
        fig_top10_products = px.bar(top10_productos, y="product_name", x="avg_delay", labels={
            'product_name': 'nombre de producto', 'avg_delay': 'demora promedio (dias)'}, orientation="h")
        fig_top10_products.update_traces(marker=dict(color=color_products))
        avg_delay_products = top10_productos["avg_delay"].mean()

        fig_top10_products.add_shape(
            type="line",
            y0=-0.5, y1=len(top10_productos) - 0.5,
            x0=avg_delay_products, x1=avg_delay_products,  # Altura de la línea
            # Configuración de la línea
            line=dict(color=LINE_COLOR, width=2, dash="dash"),
        )

        fig_top10_products.add_annotation(
            y=len(top10_productos)-3,
            x=avg_delay_products + 0.06,  # Un poco arriba de la línea
            text=f"Retraso promedio: {avg_delay_products:.1f} días",
            showarrow=False,  # No mostrar la flecha
            font=dict(size=12, color=LINE_COLOR),
            textangle=-90
        )

        st.plotly_chart(fig_top10_products)

    with total_products:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Productos con Demora Mayor a la Media", BAR_COLOR2,
                    total_productos["Total"].values[0])
with st.container():
    st.markdown("## :orange[3. Impacto en la rentabilidad] 💰")
    st.markdown(
        "### ¿Cómo afecta el retraso de un pedido a la rentabilidad de la empresa?")
    delayed, on_time = st.columns(2)
    profit = chart.get_cached_data(query.RENTABILIDAD)

    with delayed:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ganancías en demoras", BAR_COLOR2,
                    profit[profit["delivery_status"] == "Delayed"]["avg_profit"].values[0])

    with on_time:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Ganancías sin demoras", BAR_COLOR2,
                    profit[profit["delivery_status"] == "On Time"]["avg_profit"].values[0])

    st.markdown(
        "### ¿Los pedidos con descuentos o promociones tienden a experimentar más retrasos?")
    discount, no_discount = st.columns(2)
    delay_discount = chart.get_cached_data(query.DISCOUNTS)

    with discount:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Demora en items con descuento", BAR_COLOR2,
                    delay_discount[delay_discount["discount_status"] == "Discounted"]["avg_delay"].values[0])

    with no_discount:
        chart.cards(CARD_BG_COLOR, CARD_TITLE_COLOR1,
                    "Demora en items sin descuento", BAR_COLOR2,
                    delay_discount[delay_discount["discount_status"] == "No Discount"]["avg_delay"].values[0])
