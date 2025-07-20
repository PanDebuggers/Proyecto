# limpiar_tablas.py
# 🧹 Borra todos los datos de todas las tablas (sin borrar estructura)

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SQL_FILE = os.path.join(BASE_DIR, "..", "MediCareDesk_SQLite.sql")
DB_PATH = os.path.join(BASE_DIR, "..", "data", "MediCareDesk.db")

# Orden correcto: primero tablas hijas, luego padres
tablas = [
    "Toma",
    "Evento",
    "Tratamiento_Medicamento",
    "Tratamiento",
    "Cuidador_Paciente",   # 🔑 Ahora se limpia la tabla intermedia N:N
    "Paciente",
    "Medicamento",
    "Cuidador"
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    for tabla in tablas:
        try:
            cursor.execute(f"DELETE FROM {tabla};")
            print(f"✔️ Tabla '{tabla}' vaciada.")
        except sqlite3.OperationalError:
            print(f"⚠️ Tabla '{tabla}' no existe o ya fue eliminada.")
    conn.commit()
    print("\n✅ Todas las tablas limpias correctamente.")
except Exception as e:
    print("❌ Error al limpiar las tablas:", e)
finally:
    conn.close()
    print("Conexión a la base de datos cerrada.")
    print("Script de limpieza finalizado.")