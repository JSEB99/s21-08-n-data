from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Configuración de conexión
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# 5 minutos
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?options=-c%20statement_timeout=300000"

engine = create_engine(DATABASE_URL)

try:
    print("Conectando a la base de datos...")
    query = "SELECT * FROM order_facts"  # Consulta completa
    output_file = "../../data/processed/order_facts.csv"
    chunksize = 10000  # Procesar en bloques de 10,000 filas

    # Exportar por bloques
    with engine.connect() as connection:
        for i, chunk in enumerate(pd.read_sql_query(query, connection, chunksize=chunksize)):
            mode = 'w' if i == 0 else 'a'  # Escribir encabezados solo en el primer bloque
            header = i == 0
            chunk.to_csv(output_file, mode=mode, index=False, header=header)
            print(
                f"Bloque {i + 1} exportado. Total filas procesadas: {(i + 1) * chunksize}")

    print(f"Exportación completa. Archivo guardado como {output_file}.")
except Exception as e:
    print(f"Error: {e}")
