import streamlit as st
import utils.sidebar as sb

st.set_page_config(
    page_title="SupplyRisk - Prediction",
    layout="wide",
    page_icon="🤖")

sb.show_sidebar()

st.markdown('<h1 style="background-color: rgb(96, 180, 255); color: white; padding: 5px; border-radius: 5px; text-align: center;">Detección de Envío Tardío</h1>',
            unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
