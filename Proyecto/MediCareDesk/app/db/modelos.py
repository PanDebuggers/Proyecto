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
    cursor.execute("SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4]
        }
        return cuidador
    return None

def buscar_cuidador_por_credenciales(email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ? AND password_hash = ?", (email, password_hash))
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4]
        }
        return cuidador
    return None
# ----------------------------------------------------------------------------------------