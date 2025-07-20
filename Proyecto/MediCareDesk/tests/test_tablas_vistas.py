import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.conexion import obtener_conexion

class TestBaseDeDatos(unittest.TestCase):

    def test_conexion_exitosa(self):
        conn = obtener_conexion()
        self.assertIsNotNone(conn)
        conn.close()

    def test_tablas_existentes(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [tabla["name"] for tabla in cursor.fetchall()]
        esperadas = ["Paciente", "Cuidador", "Medicamento", "Tratamiento", "Tratamiento_Medicamento", "Toma", "Evento"]
        for tabla in esperadas:
            self.assertIn(tabla, tablas)
        conn.close()

    def test_vista_pacientes(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        vistas = [vista["name"] for vista in cursor.fetchall()]
        self.assertIn("Vista_Pacientes", vistas)
        conn.close()

if __name__ == '__main__':
    unittest.main()