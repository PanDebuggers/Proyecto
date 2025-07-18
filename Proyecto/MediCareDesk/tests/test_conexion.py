#verifica la conexion de la base de datos. Creado por CatherineHerrera96
from app.db.conexion import get_connection

def probar_conexion():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print("-", tabla["name"])
    conn.close()

probar_conexion()

#python -m tests.test_conexion para ejecucion (en la raiz del proyecto)