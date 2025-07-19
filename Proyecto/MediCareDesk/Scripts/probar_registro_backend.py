#Solo para pruebas manuales del registro
import sqlite3

DB_PATH = "data/MediCareDesk.db"

nuevo_cuidador = {
    "nombre": "Mariana Test",
    "relacion": "Enfermera",
    "contacto": "3100000000",
    "email": "mariana.test@example.com",
    "password": "test1234"
}

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("""
        INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nuevo_cuidador["nombre"],
        nuevo_cuidador["relacion"],
        nuevo_cuidador["contacto"],
        nuevo_cuidador["email"],
        nuevo_cuidador["password"]
    ))
    conn.commit()
    print("✅ Cuidador registrado correctamente.")
except sqlite3.IntegrityError:
    print("⚠️ Ya existe un cuidador con ese correo.")
finally:
    conn.close()
