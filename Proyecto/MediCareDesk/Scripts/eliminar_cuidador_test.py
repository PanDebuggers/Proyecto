#Limpia la tabla cuidador
import sqlite3

conn = sqlite3.connect("data/MediCareDesk.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM Cuidador")
conn.commit()
conn.close()

print("🧹 Tabla Cuidador vaciada.")
