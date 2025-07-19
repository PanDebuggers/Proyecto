from .conexion import obtener_conexion

def insertar_cuidador(nombre, relacion, contacto, email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, relacion, contacto, email, password_hash))
    conn.commit()
    conn.close()

def buscar_cuidador_por_email(email):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cuidador WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_cuidador_por_credenciales(email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cuidador WHERE email = ? AND password_hash = ?", (email, password_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado
# ----------------------------------------------------------------------------------------