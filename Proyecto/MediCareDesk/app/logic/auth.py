#Creado por CatherineHerrera96
#Manejo del Login

from app.db.conexion import get_connection

def validar_credenciales(email, password):
    """
    Verifica si existe un cuidador con ese email y contraseña.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT * FROM Cuidador
        WHERE email = ? AND password_hash = ?
    """
    cursor.execute(query, (email, password))
    cuidador = cursor.fetchone()
    conn.close()
    return cuidador is not None
