# borrar_tabla.py
# ⚠️ Borra solo UNA tabla. Edita la variable 'tabla' antes de ejecutar.

import sqlite3

tabla = "NombreTabla"  # ← Reemplaza este valor por el nombre de la tabla a limpiar
DB_PATH = "data/MediCareDesk.db"

confirm = input(f"⚠️ ¿Seguro que deseas vaciar la tabla '{tabla}'? Escribe SÍ para continuar: ")
if confirm != "SÍ":
    exit("❌ Operación cancelada.")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute(f"DELETE FROM {tabla}")
    conn.commit()
    print(f"🧹 Tabla '{tabla}' vaciada.")
except Exception as e:
    print(f"❌ Error al vaciar la tabla '{tabla}':", e)
finally:
    conn.close()
