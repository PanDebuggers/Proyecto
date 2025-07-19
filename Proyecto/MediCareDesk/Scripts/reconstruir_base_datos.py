# restaurar_base.py
# ⚠️ Elimina completamente la base MediCareDesk.db y la reconstruye desde el SQL

import sqlite3
import os

SQL_FILE = "MediCareDesk_SQLite.sql"
DB_PATH = "data/MediCareDesk.db"

confirm = input("⚠️ Esto eliminará TODA la base de datos y la reconstruirá. Escribe REINICIAR para continuar: ")
if confirm != "REINICIAR":
    exit("❌ Operación cancelada.")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🗑️ Base de datos anterior eliminada.")

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_script = f.read()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()
conn.close()

print("✅ Nueva base de datos creada exitosamente.")
