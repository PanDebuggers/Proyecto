#Creado por CatherineHerrera96
#inserta datos a Cuidador para realizar las pruebas unitarias
import sqlite3

conn = sqlite3.connect("data/MediCareDesk.db")
cursor = conn.cursor()

cursor.execute("""
    INSERT OR REPLACE INTO Cuidador (id_cuidador, nombre, relacion, contacto, email, password_hash)
    VALUES (?, ?, ?, ?, ?, ?)
""", (999, 'Catherine Herrera', 'Hija', '3214567890', 'cathy@example.com', '1234'))

conn.commit()
conn.close()

print("✅ Cuidador de prueba insertado.")
