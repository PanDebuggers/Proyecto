# app/db/conexion.py

import sqlite3
import os

DB_FILENAME = "data/MediCareDesk.db"

def obtener_conexion():
    db_path = os.path.abspath(DB_FILENAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn




