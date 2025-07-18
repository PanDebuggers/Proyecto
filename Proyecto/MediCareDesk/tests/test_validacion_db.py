#Verifica la conexion de la base de datos. Creado por CatherineHerrera96
import sqlite3
import os

# Ruta esperada de la base de datos
DB_PATH = "data/MediCareDesk.db"

# Verifica si existe
if not os.path.exists(DB_PATH):
    print("❌ La base de datos no existe en la ruta:", DB_PATH)
else:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta para obtener todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()

    print("✅ Base de datos conectada correctamente.")
    print("Tablas encontradas:")
    for tabla in tablas:
        print(" -", tabla[0])

    conn.close()
