import streamlit as st
import utils.sidebar as sb

st.set_page_config(
    page_title="SupplyRisk - Contact",
    layout="centered",
    page_icon="📩")

sb.show_sidebar()

st.markdown('<h1 style="background-color: rgb(96, 180, 255); color: white; padding: 5px; border-radius: 5px; text-align: center;">Información del equipo</h1>',
            unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<h3 style="color:orange">Integrantes:</h2>',
            unsafe_allow_html=True)
st.divider()
name, role, github, linkedin = st.columns(4)

name.markdown(
    '<h5 style="background-color: rgb(96,180,255); padding: 2px; border-radius: 4px;text-align: center; margin-bottom: 15px;">Nombre</h5>',
    unsafe_allow_html=True)
role.markdown(
    '<h5 style="background-color: rgb(96,180,255); padding: 2px; border-radius: 4px;text-align: center;margin-bottom: 15px;">Rol</h5>',
    unsafe_allow_html=True)
github.markdown(
    '<h5 style="background-color: rgb(96,180,255); padding: 2px; border-radius: 4px;text-align: center;margin-bottom: 15px;">GitHub</h5>',
    unsafe_allow_html=True)
linkedin.markdown(
    '<h5 style="background-color: rgb(96,180,255); padding: 2px; border-radius: 4px;text-align: center;margin-bottom: 15px;">LinkedIn</h5>',
    unsafe_allow_html=True)

name.write("Sebastian Mora")
role.write("Ingeniero de Datos")
github.markdown('[GitHub](https://github.com/JSEB99)')
linkedin.markdown('[LinkedIn](https://www.linkedin.com/in/jsebastianm/)')
name.write("Livan Gonzalez")
role.write("Analista de Datos")
github.markdown('[GitHub](https://github.com/R3dsm1le)')
linkedin.markdown('[LinkedIn](https://www.linkedin.com/in/red-smile-/)')
name.write("Juan Guerrero")
role.write("Cientifico de Datos")
github.markdown('[GitHub](https://github.com/juanvicente0104)')
linkedin.markdown('[LinkedIn](https://www.linkedin.com/in/juanvicente0104/)')
name.write("Brayan Cordoba")
role.write("Cientifico de Datos")
github.markdown('[GitHub](https://github.com/brayan-cordova)')
linkedin.markdown('[LinkedIn](https://www.linkedin.com/in/bcordovag/)')
