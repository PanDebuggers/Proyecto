# Creado por CatherineHerrera96
# Conexión a SQLite y existencia de tablas. SI ACCEDE A LA BASE DE DATOS
# Este TEST no hace parte de las pruebas unitarias, es Solo para confirmar la adecuada conexion de la base de datos
import unittest
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
)
from app.db.conexion import get_connection


class TestBaseDeDatos(unittest.TestCase):

    def test_conexion_exitosa(self):
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_tablas_existentes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [tabla["name"] for tabla in cursor.fetchall()]
        esperadas = [
            "Paciente",
            "Cuidador",
            "Medicamento",
            "Tratamiento",
            "Tratamiento_Medicamento",
            "Toma",
            "Evento",
        ]
        for tabla in esperadas:
            self.assertIn(tabla, tablas)
        conn.close()


if __name__ == "__main__":
    unittest.main()


# python -m tests.test_conexion para ejecucion (en la raiz del proyecto)
