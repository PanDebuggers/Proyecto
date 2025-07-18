#Creado por CatherineHerrera96
"""
Script para reconstruir completamente la base de datos MediCareDesk.db

Úsalo SOLO si deseas eliminar todo y empezar desde cero.

Pasos:
1. Asegúrate de que el archivo MediCareDesk_SQLite.sql esté actualizado.
2. Borra (o renombra) el archivo data/MediCareDesk.db si ya existe.
3. Ejecuta este script.

Resultado: se creará una nueva base de datos vacía con todas las tablas definidas en el SQL.
"""

import sqlite3
import os

# Ruta del archivo SQL
SQL_FILE = "MediCareDesk_SQLite.sql"
DB_PATH = "data/MediCareDesk.db"

# Paso 1: borrar el archivo si ya existe
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🗑️ Base de datos anterior eliminada.")

# Paso 2: cargar el script SQL
with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Paso 3: crear la base de datos y ejecutar el script
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()

print("✅ Nueva base de datos creada exitosamente.")
