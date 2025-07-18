# Creado por CatherineHerrera96
#Conexion de la base de datos. 

import sqlite3
import os

# Ruta relativa al archivo de base de datos
DB_FILENAME = "data/MediCareDesk.db"

def get_connection():
    """
    Abre una conexión a la base de datos SQLite.
    Retorna una conexión lista para ejecutar queries.
    """
    db_path = os.path.abspath(DB_FILENAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn
