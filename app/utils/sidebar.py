import streamlit as st


def show_sidebar():
    st.sidebar.header("Supply**Risk** :blue[AI]", divider="blue")

    st.sidebar.page_link("0_home.py", label="🏠 Inicio")
    st.sidebar.page_link("pages/1_analysis.py", label="📊 Análisis de datos")
    st.sidebar.page_link("pages/2_prediction.py",
                         label="🔍 Predicción de datos")
    st.sidebar.page_link("pages/3_contact.py", label="📩 Contacto")

    st.sidebar.header("Equipo 🤝", divider="blue")
    st.sidebar.subheader(":orange[s21-08-n-data]")

    st.sidebar.link_button(label="Proyecto en GitHub",
                           url="https://github.com/No-Country-simulation/s21-08-n-data",
                           type="secondary")
