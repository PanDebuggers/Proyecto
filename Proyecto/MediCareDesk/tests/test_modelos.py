import unittest
from app.db import modelos


class TestModelosCuidador(unittest.TestCase):

    def setUp(self):
        """Limpia cualquier entrada de prueba previa."""
        conn = modelos.obtener_conexion()
        conn.execute("DELETE FROM Cuidador WHERE email = 'prueba@correo.com'")
        conn.commit()
        conn.close()

    def test_insertar_cuidador(self):
        """Debe insertar un cuidador correctamente en la base de datos."""
        modelos.insertar_cuidador(
            nombre="Cuidador Prueba",
            relacion="Hermano",
            contacto="3011111111",
            email="prueba@correo.com",
            password_hash="clave123",
        )
        resultado = modelos.buscar_cuidador_por_email("prueba@correo.com")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[1], "Cuidador Prueba")  # índice 1 = nombre

    def test_buscar_cuidador_por_credenciales_correctas(self):
        """Debe retornar el cuidador si las credenciales son correctas."""
        modelos.insertar_cuidador(
            nombre="Cuidador Prueba",
            relacion="Hermano",
            contacto="3011111111",
            email="prueba@correo.com",
            password_hash="clave123",
        )
        resultado = modelos.buscar_cuidador_por_credenciales(
            "prueba@correo.com", "clave123"
        )
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[1], "Cuidador Prueba")

    def test_buscar_cuidador_por_credenciales_incorrectas(self):
        """Debe retornar None si las credenciales son inválidas."""
        resultado = modelos.buscar_cuidador_por_credenciales(
            "noexiste@correo.com", "nada"
        )
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()

# ---------------------------------------------------------------------------------------
