# limpiar_tablas.py
# 🧹 Borra todos los datos de todas las tablas (no borra estructura ni el archivo .db)

import sqlite3

DB_PATH = "data/MediCareDesk.db"

tablas = [
    "Toma",
    "Evento",
    "Tratamiento_Medicamento",
    "Tratamiento",
    "Medicamento",
    "Paciente",
    "Cuidador"
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    for tabla in tablas:
        try:
            cursor.execute(f"DELETE FROM {tabla}")
            print(f"✔️ Tabla '{tabla}' vaciada.")
        except sqlite3.OperationalError:
            print(f"⚠️ Tabla '{tabla}' no existe o ya fue eliminada.")
    conn.commit()
    print("✅ Todas las tablas limpias.")
except Exception as e:
    print("❌ Error al limpiar las tablas:", e)
finally:
    conn.close()
