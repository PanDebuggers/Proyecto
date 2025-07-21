import sys
import os
from pathlib import Path
import unittest
import sqlite3


# Solución permanente para imports
root_path = str(Path(__file__).parent.parent)
sys.path.append(root_path)

from app.db import modelos
#
print(">>> test_tratamientos.py ejecutándose desde:", __file__)

print(">>> modelos.py cargado desde:", modelos.__file__)
print(">>> funciones en modelos:", dir(modelos))

#
import importlib
import app.db.modelos
importlib.reload(app.db.modelos)
from app.db import modelos
# 
from app.logic import tratamientos
print(">>> tratamientos.py cargado desde:", tratamientos.__file__)
from datetime import datetime, timedelta

class TestTratamientos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        # Configurar conexión a BD en memoria
        modelos.conexion = sqlite3.connect(":memory:")
        modelos.conexion.row_factory = sqlite3.Row
        
        # Crear tablas
        with open(Path(__file__).parent.parent / 'MediCareDesk_SQLite.sql', 'r') as f:

            sql = f.read()
        modelos.conexion.executescript(sql)
        modelos.conexion.commit()
        
        # Datos de prueba
        cursor = modelos.conexion.cursor()
        
        # Insertar paciente
        cursor.execute("""
            INSERT INTO Paciente (nombre, edad, genero)
            VALUES ('Paciente Prueba', 30, 'M')
        """)
        cls.paciente_id = cursor.lastrowid
        
        # Insertar medicamento
        cursor.execute("""
            INSERT INTO Medicamento (nombre, presentacion)
            VALUES ('Medicamento Prueba', 'Comprimidas')
        """)
        cls.medicamento_id = cursor.lastrowid
        
        # Insertar tratamiento
        cursor.execute("""
            INSERT INTO Tratamiento (id_paciente, nombre_tratamiento, fecha_inicio, fecha_fin, estado)
            VALUES (?, 'Tratamiento Prueba', '2023-01-01', '2023-01-10', 'activo')
        """, (cls.paciente_id,))
        cls.tratamiento_id = cursor.lastrowid
        
        modelos.conexion.commit()
    
    def test_1_asignar_medicamento_valido(self):
        """Prueba asignación válida de medicamento - Versión corregida"""
        # Verificar que el tratamiento existe primero
        tratamiento = modelos.obtener_tratamiento(self.tratamiento_id)
        self.assertIsNotNone(tratamiento, "El tratamiento de prueba no existe")
        
        # Verificar que el medicamento existe
        medicamento = modelos.obtener_medicamento(self.medicamento_id)
        self.assertIsNotNone(medicamento, "El medicamento de prueba no existe")
        
        # Datos de prueba
        datos_asignacion = {
            'id_tratamiento': self.tratamiento_id,
            'id_medicamento': self.medicamento_id,
            'dosis': '1 tableta',
            'frecuencia': 'una_vez_al_dia',
            'via_administracion': 'oral',
            'hora_preferida': '08:00',
            'estado': 'activo'
        }
        
        # Asignar medicamento
        asignacion_id = tratamientos.asignar_medicamento_a_tratamiento(**datos_asignacion)
        
        # Verificaciones
        self.assertIsInstance(asignacion_id, int)
        self.assertGreater(asignacion_id, 0)
        
        # Verificar en BD
        asignacion = modelos.obtener_tratamiento_medicamento(asignacion_id)
        self.assertIsNotNone(asignacion)
        self.assertEqual(asignacion['id_tratamiento'], self.tratamiento_id)
        self.assertEqual(asignacion['id_medicamento'], self.medicamento_id)


    def test_2_generar_tomas_automaticas(self):
        """Prueba generación automática de tomas"""
        # Primero asignamos el medicamento
        asignacion_id = tratamientos.asignar_medicamento_a_tratamiento(
            id_tratamiento=self.tratamiento_id,
            id_medicamento=self.medicamento_id,
            dosis='1 tableta',
            frecuencia='una_vez_al_dia',
            via_administracion='oral',
            hora_preferida='08:00',
            estado='activo'
        )
        
        # Generar tomas
        tratamientos.generar_tomas_tratamiento(asignacion_id)
        
        # Verificar que se generaron las tomas
        cursor = modelos.conexion.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM Toma 
            WHERE id_tratamiento_medicamento = ?
        """, (asignacion_id,))
        count = cursor.fetchone()['count']
        self.assertEqual(count, 10)  # 10 días de tratamiento
        
        # Verificar primera y última toma
        cursor.execute("""
            SELECT * FROM Toma 
            WHERE id_tratamiento_medicamento = ?
            ORDER BY fecha, hora_programada
            LIMIT 1
        """, (asignacion_id,))
        primera_toma = cursor.fetchone()
        self.assertEqual(primera_toma['fecha'], '2023-01-01')
        self.assertEqual(primera_toma['hora_programada'], '08:00:00')
        
        cursor.execute("""
            SELECT * FROM Toma 
            WHERE id_tratamiento_medicamento = ?
            ORDER BY fecha DESC, hora_programada DESC
            LIMIT 1
        """, (asignacion_id,))
        ultima_toma = cursor.fetchone()
        self.assertEqual(ultima_toma['fecha'], '2023-01-10')
    
def test_3_validacion_fechas_invalidas(self):
    """Prueba que no se puedan asignar horas y fechas inconsistentes"""
    # Caso 1: Hora inválida (formato incorrecto)
    with self.assertRaises(ValueError) as context:
        tratamientos.asignar_medicamento_a_tratamiento(
            id_tratamiento=self.tratamiento_id,
            id_medicamento=self.medicamento_id,
            dosis='1 tableta',
            frecuencia='una_vez_al_dia',
            via_administracion='oral',
            hora_preferida='25:00',  # Hora inválida
            estado='activo'
        )
    self.assertIn("Hora inválida", str(context.exception))
    
    # Caso 2: Hora inválida (formato incorrecto)
    with self.assertRaises(ValueError) as context:
        tratamientos.asignar_medicamento_a_tratamiento(
            id_tratamiento=self.tratamiento_id,
            id_medicamento=self.medicamento_id,
            dosis='1 tableta',
            frecuencia='una_vez_al_dia',
            via_administracion='oral',
            hora_preferida='abc',  # Formato inválido
            estado='activo'
        )
    self.assertIn("Formato de hora inválido", str(context.exception))
    
    # Caso 3: Fecha fin anterior a fecha inicio
    with self.assertRaises(ValueError) as context:
        tratamientos.asignar_medicamento_a_tratamiento(
            id_tratamiento=self.tratamiento_id,
            id_medicamento=self.medicamento_id,
            dosis='1 tableta',
            frecuencia='una_vez_al_dia',
            via_administracion='oral',
            hora_preferida='08:00',
            estado='activo',
            fecha_inicio='2023-02-01',
            fecha_fin='2023-01-01'  # Fecha fin anterior
        )
    self.assertIn("no puede ser anterior", str(context.exception))
    
    # Caso 4: Formato de fecha inválido
    with self.assertRaises(ValueError) as context:
        tratamientos.asignar_medicamento_a_tratamiento(
            id_tratamiento=self.tratamiento_id,
            id_medicamento=self.medicamento_id,
            dosis='1 tableta',
            frecuencia='una_vez_al_dia',
            via_administracion='oral',
            hora_preferida='08:00',
            estado='activo',
            fecha_inicio='2023/02/01',  # Formato inválido
            fecha_fin='2023-01-01'
        )
    self.assertIn("Formato de fecha inválido", str(context.exception))
    
    @classmethod
    def tearDownClass(cls):
        """Limpieza después de todas las pruebas"""
        modelos.conexion.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)