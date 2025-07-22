import sys
import os

# Forzar sys.path para que apunte a la carpeta donde está 'app'
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "MediCareDesk")
    ),
)

import sqlite3
from datetime import datetime, timedelta

# Importar la lógica de tratamientos usando el path original
from app.logic import tratamientos as logic_tratamientos

# Ruta a tu DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "MediCareDesk.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Insertar 2 cuidadores solo si no existen
    cuidadores = [
        ("Ana Pérez", "Hija", "3214567890", "ana@example.com", "hash123"),
        ("Luis Gómez", "Nieto", "9876543210", "luis@example.com", "hash456"),
    ]
    for nombre, relacion, contacto, email, password_hash in cuidadores:
        cursor.execute("SELECT 1 FROM Cuidador WHERE email = ?", (email,))
        if not cursor.fetchone():
            cursor.execute(
                """
                INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
                VALUES (?, ?, ?, ?, ?)
            """,
                (nombre, relacion, contacto, email, password_hash),
            )

    # Obtener sus IDs
    cursor.execute(
        "SELECT id_cuidador FROM Cuidador WHERE email = ?", ("ana@example.com",)
    )
    cuidador1_id = cursor.fetchone()[0]
    cursor.execute(
        "SELECT id_cuidador FROM Cuidador WHERE email = ?", ("luis@example.com",)
    )
    cuidador2_id = cursor.fetchone()[0]

    # Insertar pacientes (sin id_cuidador directo)
    pacientes_info = [
        ("Pedro Ruiz", 70, "M", "123456789", "Hipertenso"),
        ("María López", 80, "F", "987654321", "Diabetes"),
        ("Carlos Pérez", 75, "M", "456789123", "Alzheimer"),
        ("Juana Torres", 68, "F", "321654987", "Artrosis"),
        ("Ramón Díaz", 72, "M", "654987321", "Parkinson"),
        ("Lucía Rojas", 78, "F", "789321654", "Problemas cardíacos"),
    ]

    pacientes_ids = []

    for i, paciente in enumerate(pacientes_info):
        cursor.execute(
            """
            INSERT INTO Paciente (nombre, edad, genero, contacto_emergencia, observaciones)
            VALUES (?, ?, ?, ?, ?)
        """,
            paciente,
        )
        paciente_id = cursor.lastrowid
        pacientes_ids.append(paciente_id)

        # Asignar relación en tabla intermedia:
        if i < 3:
            cursor.execute(
                """
                INSERT INTO Cuidador_Paciente (id_cuidador, id_paciente)
                VALUES (?, ?)
            """,
                (cuidador1_id, paciente_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO Cuidador_Paciente (id_cuidador, id_paciente)
                VALUES (?, ?)
            """,
                (cuidador2_id, paciente_id),
            )

    # Insertar un medicamento genérico
    cursor.execute(
        """
        INSERT INTO Medicamento (nombre, principio_activo, indicaciones, fecha_caducidad, contraindicaciones, presentacion, laboratorio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "Paracetamol",
            "Paracetamol 500mg",
            "Tomar cada 8 horas",
            (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "Hígado",
            "Comprimidas",
            "Lab Genérico",
        ),
    )
    medicamento_id = cursor.lastrowid

    # Insertar tratamiento y asignarlo a medicamento para cada paciente
    for paciente_id in pacientes_ids:
        cursor.execute(
            """
            INSERT INTO Tratamiento (id_paciente, nombre_tratamiento, descripcion, estado, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                paciente_id,
                "Tratamiento Básico",
                "Control de dolor y fiebre",
                "activo",
                datetime.now().strftime("%Y-%m-%d"),
                (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            ),
        )
        tratamiento_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO Tratamiento_Medicamento
            (id_tratamiento, id_medicamento, dosis, frecuencia, via_administracion, fecha_inicio, fecha_fin, estado, hora_preferida)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                tratamiento_id,
                medicamento_id,
                "500mg",
                "cada_8_horas",
                "oral",
                datetime.now().strftime("%Y-%m-%d"),
                (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "activo",
                "08:00",
            ),
        )
        asignacion_id = cursor.lastrowid
        # Hacer commit antes de llamar a la lógica de generación de tomas
        conn.commit()
        # Generar tomas programadas usando la lógica de la app
        try:
            logic_tratamientos.generar_tomas_tratamiento(asignacion_id)
        except Exception as e:
            print(
                f"[ADVERTENCIA] No se pudieron generar tomas para asignacion_id={asignacion_id}: {e}"
            )

    conn.commit()
    print("✅ Datos de prueba insertados correctamente.")

except sqlite3.Error as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
