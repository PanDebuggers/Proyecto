# creado por CatherineHerrera96
from app.db.conexion import get_connection

def validar_credenciales(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Cuidador WHERE email = ? AND password_hash = ?"
    cursor.execute(query, (email, password))
    cuidador = cursor.fetchone()
    conn.close()
    return cuidador is not None

def obtener_cuidador_por_email(email):
    """
    Retorna el registro completo del cuidador según su email.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cuidador WHERE email = ?", (email,))
    cuidador = cursor.fetchone()
    conn.close()
    return cuidador
