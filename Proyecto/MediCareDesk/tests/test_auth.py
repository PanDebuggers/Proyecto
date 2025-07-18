#Creado por CatherineHerrera96

import unittest
from app.logic.auth import validar_credenciales

class TestAuth(unittest.TestCase):
    def test_login_correcto(self):
        """Debe autenticar a un cuidador con credenciales válidas."""
        self.assertTrue(validar_credenciales("cathy@example.com", "1234"))

    def test_login_email_invalido(self):
        """Debe fallar si el email no está registrado."""
        self.assertFalse(validar_credenciales("noexiste@example.com", "1234"))

    def test_login_password_incorrecta(self):
        """Debe fallar si la contraseña no es correcta."""
        self.assertFalse(validar_credenciales("cathy@example.com", "clave_incorrecta"))

if __name__ == "__main__":
    unittest.main()
