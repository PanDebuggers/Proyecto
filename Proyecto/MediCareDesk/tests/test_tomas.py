# Creado por GitHub Copilot

import unittest
from app.logic.tomas import registrar_toma, obtener_tomas_por_cuidador, obtener_alertas_tomas

class TestTomas(unittest.TestCase):
    def test_registro_toma_exitoso(self):
        """Debe registrar una toma correctamente y devolver True."""
        resultado = registrar_toma(cuidador_id=1, medicamento_id=2, fecha="2025-07-24", hora="08:00")
        self.assertTrue(resultado)

    def test_registro_toma_faltan_datos(self):
        """Debe fallar si faltan datos obligatorios."""
        resultado = registrar_toma(cuidador_id=None, medicamento_id=2, fecha="2025-07-24", hora="08:00")
        self.assertFalse(resultado)

    def test_historial_tomas(self):
        """Debe devolver una lista de tomas para un cuidador existente."""
        tomas = obtener_tomas_por_cuidador(cuidador_id=1)
        self.assertIsInstance(tomas, list)
        self.assertGreaterEqual(len(tomas), 0)

    def test_alertas_tomas(self):
        """Debe devolver una lista de alertas de tomas para un cuidador."""
        alertas = obtener_alertas_tomas(cuidador_id=1)
        self.assertIsInstance(alertas, list)
        self.assertGreaterEqual(len(alertas), 0)

if __name__ == "__main__":
    unittest.main()
