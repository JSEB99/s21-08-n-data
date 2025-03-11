from sqlalchemy import create_engine
import pandas as pd
import streamlit as st


@st.cache_resource()
def connection():

    USER = st.secrets["database"]["user"]
    PASSWORD = st.secrets["database"]["password"]
    HOST = st.secrets["database"]["host"]
    PORT = st.secrets["database"]["port"]
    DBNAME = st.secrets["database"]["dbname"]

    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

    return create_engine(DATABASE_URL)


def fetch_data(query):
    engine = connection()
    try:
        print("Conectando a la base de datos...")
        with engine.connect() as connection_db:
            print("Conexión establecida. Ejecutando consulta...")
            df = pd.read_sql_query(query, connection_db)
            print("Consulta ejecutada correctamente.")
        return df
    except Exception as e:
        print(f"Error: {e}")


@st.cache_data()
def get_cached_data(query):
    return fetch_data(query)


def cards(bg_color, title_color, title, value_color, value, value_font_size="30px"):
    card = st.markdown(f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 10px;
            height: 100px;  /* Ajustar el alto de la tarjeta */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;;
        ">
            <div style="font-size: 12px; font-weight: bold; height: 30%;
            display: flex; align-items: center; justify-content: center;
            margin-bottom: 10px; text-align: center;color:{title_color}">
                {title}
            </div>
            <div style="font-size: {value_font_size}; color: {value_color};
                        font-weight: bold; height: 70%; display: flex;
                        align-items: center; justify-content: center;">
                {value}
            </div>
        </div>
    """, unsafe_allow_html=True)
    return card
