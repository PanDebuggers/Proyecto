# Obtener la próxima toma semanal de cada paciente del cuidador
def obtener_proximas_tomas_semanales_por_paciente(id_cuidador):
    import datetime

    hoy = datetime.date.today()
    fecha_inicio = hoy.isoformat()
    fecha_fin = (hoy + datetime.timedelta(days=6)).isoformat()
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Obtener todos los pacientes del cuidador
    cursor.execute(
        """
        SELECT p.id_paciente, p.nombre
        FROM Paciente p
        JOIN Cuidador_Paciente cp ON cp.id_paciente = p.id_paciente
        WHERE cp.id_cuidador = ?
    """,
        (id_cuidador,),
    )
    pacientes = cursor.fetchall()
    proximas_tomas = []
    for id_paciente, nombre_paciente in pacientes:
        cursor.execute(
            """
            SELECT Toma.id_toma, Toma.fecha, Toma.hora_programada, Toma.estado,
                   Medicamento.nombre AS nombre_medicamento
            FROM Toma
            JOIN Tratamiento_Medicamento ON Toma.id_tratamiento_medicamento = Tratamiento_Medicamento.id_tratamiento_medicamento
            JOIN Tratamiento ON Tratamiento_Medicamento.id_tratamiento = Tratamiento.id_tratamiento
            JOIN Medicamento ON Tratamiento_Medicamento.id_medicamento = Medicamento.id_medicamento
            WHERE Tratamiento.id_paciente = ?
              AND Toma.fecha >= ? AND Toma.fecha <= ?
              AND Toma.estado = 'programada'
            ORDER BY Toma.fecha ASC, Toma.hora_programada ASC
        """,
            (id_paciente, fecha_inicio, fecha_fin),
        )
        tomas_paciente = cursor.fetchall()
        if tomas_paciente:
            # Agrupar por fecha/hora y tomar la más próxima
            primera_toma = tomas_paciente[0]
            toma = dict(zip([col[0] for col in cursor.description], primera_toma))
            toma["nombre_paciente"] = nombre_paciente
            proximas_tomas.append(toma)
    if conn is not globals().get("conexion", None):
        conn.close()
    return proximas_tomas


# Obtener todas las tomas programadas para los próximos 7 días para los pacientes de un cuidador
def obtener_tomas_semana_por_cuidador(id_cuidador):
    import datetime

    hoy = datetime.date.today()
    fecha_inicio = hoy.isoformat()
    fecha_fin = (hoy + datetime.timedelta(days=6)).isoformat()
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT Toma.id_toma, Toma.fecha, Toma.hora_programada, Toma.estado,
               Paciente.nombre AS nombre_paciente, Medicamento.nombre AS nombre_medicamento
        FROM Toma
        JOIN Tratamiento_Medicamento ON Toma.id_tratamiento_medicamento = Tratamiento_Medicamento.id_tratamiento_medicamento
        JOIN Tratamiento ON Tratamiento_Medicamento.id_tratamiento = Tratamiento.id_tratamiento
        JOIN Paciente ON Tratamiento.id_paciente = Paciente.id_paciente
        JOIN Medicamento ON Tratamiento_Medicamento.id_medicamento = Medicamento.id_medicamento
        JOIN Cuidador_Paciente cp ON cp.id_paciente = Paciente.id_paciente
        WHERE Toma.fecha >= ? AND Toma.fecha <= ?
          AND cp.id_cuidador = ?
        ORDER BY Toma.fecha ASC, Toma.hora_programada ASC
    """
    cursor.execute(query, (fecha_inicio, fecha_fin, id_cuidador))
    tomas = [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tomas


def buscar_cuidador_por_id(id_cuidador):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE id_cuidador = ?",
        (id_cuidador,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4],
        }
        return cuidador
    return None


# Consultar historial de tomas por paciente
def obtener_historial_tomas_paciente(id_paciente):
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT Toma.id_toma, Toma.fecha, Toma.hora_programada, Toma.estado, 
               Medicamento.nombre AS nombre_medicamento,
               COALESCE(Toma.verificada, 0) AS verificada
        FROM Toma
        JOIN Tratamiento_Medicamento ON Toma.id_tratamiento_medicamento = Tratamiento_Medicamento.id_tratamiento_medicamento
        JOIN Tratamiento ON Tratamiento_Medicamento.id_tratamiento = Tratamiento.id_tratamiento
        JOIN Medicamento ON Tratamiento_Medicamento.id_medicamento = Medicamento.id_medicamento
        WHERE Tratamiento.id_paciente = ?
        ORDER BY Toma.fecha DESC, Toma.hora_programada DESC
    """
    cursor.execute(query, (id_paciente,))
    tomas = [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tomas


# Obtener la toma más cercana de cada paciente para hoy
def obtener_tomas_mas_cercanas_por_paciente(id_cuidador):
    import datetime

    ahora = datetime.datetime.now()
    fecha = ahora.date().isoformat()
    conn = obtener_conexion()
    cursor = conn.cursor()
    # Subconsulta: para cada paciente, obtener la toma programada más próxima a la hora actual
    query = """
        SELECT t1.id_toma, t1.fecha, t1.hora_programada, t1.estado,
               p.nombre AS nombre_paciente, m.nombre AS nombre_medicamento
        FROM Toma t1
        JOIN Tratamiento_Medicamento tm ON t1.id_tratamiento_medicamento = tm.id_tratamiento_medicamento
        JOIN Tratamiento tto ON tm.id_tratamiento = tto.id_tratamiento
        JOIN Paciente p ON tto.id_paciente = p.id_paciente
        JOIN Medicamento m ON tm.id_medicamento = m.id_medicamento
        JOIN Cuidador_Paciente cp ON cp.id_paciente = p.id_paciente
        WHERE t1.fecha = ?
          AND cp.id_cuidador = ?
          AND t1.estado = 'programada'
          AND t1.hora_programada = (
              SELECT MIN(t2.hora_programada)
              FROM Toma t2
              JOIN Tratamiento_Medicamento tm2 ON t2.id_tratamiento_medicamento = tm2.id_tratamiento_medicamento
              JOIN Tratamiento tto2 ON tm2.id_tratamiento = tto2.id_tratamiento
              WHERE t2.fecha = ?
                AND tto2.id_paciente = p.id_paciente
                AND t2.estado = 'programada'
                AND t2.hora_programada >= ?
          )
        ORDER BY t1.hora_programada ASC
    """
    hora_actual = ahora.strftime("%H:%M")
    cursor.execute(query, (fecha, id_cuidador, fecha, hora_actual))
    tomas = [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tomas


# Tomas próximas a vencer (ejemplo: próximas en la siguiente hora)
import datetime


def obtener_tomas_proximas(id_cuidador, minutos=60):
    """
    Obtiene tomas programadas para hoy que están próximas a vencer (en los próximos X minutos).
    """
    ahora = datetime.datetime.now()
    fecha = ahora.date().isoformat()
    hora_actual = ahora.strftime("%H:%M")
    hora_limite = (ahora + datetime.timedelta(minutes=minutos)).strftime("%H:%M")
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT Toma.id_toma, Toma.fecha, Toma.hora_programada, Toma.estado, 
               Paciente.nombre AS nombre_paciente, Medicamento.nombre AS nombre_medicamento
        FROM Toma
        JOIN Tratamiento_Medicamento ON Toma.id_tratamiento_medicamento = Tratamiento_Medicamento.id_tratamiento_medicamento
        JOIN Tratamiento ON Tratamiento_Medicamento.id_tratamiento = Tratamiento.id_tratamiento
        JOIN Paciente ON Tratamiento.id_paciente = Paciente.id_paciente
        JOIN Medicamento ON Tratamiento_Medicamento.id_medicamento = Medicamento.id_medicamento
        JOIN Cuidador_Paciente cp ON cp.id_paciente = Paciente.id_paciente
        WHERE Toma.fecha = ?
          AND cp.id_cuidador = ?
          AND Toma.estado = 'programada'
          AND Toma.hora_programada >= ?
          AND Toma.hora_programada <= ?
        ORDER BY Toma.hora_programada ASC
    """
    cursor.execute(query, (fecha, id_cuidador, hora_actual, hora_limite))
    tomas = [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tomas


# Actualizar el estado de una toma
def actualizar_estado_toma(id_toma, nuevo_estado):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Toma SET estado = ? WHERE id_toma = ?
    """,
        (nuevo_estado, id_toma),
    )
    conn.commit()
    if conn is not globals().get("conexion", None):
        conn.close()


from .conexion import obtener_conexion


def insertar_cuidador(nombre, relacion, contacto, email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """,
        (nombre, relacion, contacto, email, password_hash),
    )
    conn.commit()
    conn.close()


def buscar_cuidador_por_email(email):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ?",
        (email,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4],
        }
        return cuidador
    return None


def buscar_cuidador_por_credenciales(email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ? AND password_hash = ?",
        (email, password_hash),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4],
        }
        return cuidador
    return None


# ----------------------------------------------------------------------------------------


# def obtener_conexion():
#    import sqlite3
#    import os
#    # Si estamos corriendo pruebas, usar la conexión global en memoria
#    if os.getenv("TESTING") == "0":
#        if 'conexion' in globals() and globals()['conexion'] is not None:
#            return globals()['conexion']
#    # Producción o ejecución normal
#    return sqlite3.connect("MediCareDesk.db")


def obtener_pacientes(activos=True):
    """Obtiene todos los pacientes (solo activos por defecto)"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = "SELECT * FROM Paciente"
    if activos:
        query += " WHERE activo = 1"
    cursor.execute(query)
    pacientes = [dict(paciente) for paciente in cursor.fetchall()]
    if conn is not globals().get("conexion", None):
        conn.close()
    return pacientes


def obtener_medicamento(medicamento_id):
    """Obtiene un medicamento específico por ID"""
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Medicamento WHERE id_medicamento = ?", (medicamento_id,)
        )
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    finally:
        if conn is not globals().get("conexion", None):
            conn.close()


def obtener_medicamentos():
    """Obtiene todos los medicamentos"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Medicamento")
    medicamentos = [dict(med) for med in cursor.fetchall()]
    if conn is not globals().get("conexion", None):
        conn.close()
    return medicamentos


def obtener_tratamientos(paciente_id=None):
    """Obtiene todos los tratamientos, opcionalmente filtrados por paciente"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = "SELECT * FROM Tratamiento"
    if paciente_id:
        query += " WHERE id_paciente = ?"
        cursor.execute(query, (paciente_id,))
    else:
        cursor.execute(query)
    tratamientos = [dict(trat) for trat in cursor.fetchall()]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tratamientos


def crear_tratamiento(datos):
    """Crea un nuevo tratamiento"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Tratamiento (id_paciente, nombre_tratamiento, descripcion, 
                               estado, fecha_inicio, fecha_fin)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            datos["id_paciente"],
            datos["nombre_tratamiento"],
            datos.get("descripcion", ""),
            datos["estado"],
            datos["fecha_inicio"],
            datos["fecha_fin"],
        ),
    )
    conn.commit()
    tratamiento_id = cursor.lastrowid
    if conn is not globals().get("conexion", None):
        conn.close()
    return tratamiento_id


def obtener_tratamiento(tratamiento_id):
    """Obtiene un tratamiento específico por ID"""
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Tratamiento WHERE id_tratamiento = ?", (tratamiento_id,)
        )
        resultado = cursor.fetchone()
        if resultado:
            # Convertir a diccionario y asegurar los tipos de fecha
            tratamiento = dict(resultado)
            tratamiento["fecha_inicio"] = str(
                tratamiento["fecha_inicio"]
            )  # Asegurar string
            tratamiento["fecha_fin"] = str(tratamiento["fecha_fin"])  # Asegurar string
            return tratamiento
        return None
    finally:
        if conn is not globals().get("conexion", None):
            conn.close()


def crear_tratamiento_medicamento(datos):
    """Crea una nueva asignación tratamiento-medicamento"""
    conn = obtener_conexion()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Tratamiento_Medicamento (
                    id_tratamiento, id_medicamento, dosis, frecuencia, 
                    via_administracion, fecha_inicio, fecha_fin, estado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    datos["id_tratamiento"],
                    datos["id_medicamento"],
                    datos.get("dosis", ""),
                    datos["frecuencia"],
                    datos["via_administracion"],
                    datos.get("fecha_inicio"),
                    datos.get("fecha_fin"),
                    datos["estado"],
                ),
            )
            return cursor.lastrowid
    finally:
        if conn is not globals().get("conexion", None):
            conn.close()


def obtener_tratamiento_medicamento(asignacion_id):
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                id_tratamiento_medicamento, 
                id_tratamiento, 
                id_medicamento, 
                dosis, 
                frecuencia, 
                via_administracion,
                fecha_inicio, 
                fecha_fin, 
                estado,
                COALESCE(hora_preferida, '08:00') AS hora_preferida  -- Convertir NULL a valor predeterminado
            FROM Tratamiento_Medicamento 
            WHERE id_tratamiento_medicamento = ?
        """,
            (asignacion_id,),
        )
        row = cursor.fetchone()
        if row:
            asignacion = dict(zip([col[0] for col in cursor.description], row))
            # Convertir fechas a string
            if asignacion.get("fecha_inicio"):
                asignacion["fecha_inicio"] = str(asignacion["fecha_inicio"])
            if asignacion.get("fecha_fin"):
                asignacion["fecha_fin"] = str(asignacion["fecha_fin"])
            return asignacion
        return None
    finally:
        if conn is not globals().get("conexion", None):
            conn.close()


def crear_toma(datos):
    """Crea una nueva toma programada"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Toma (id_tratamiento_medicamento, fecha, hora_programada, estado)
        VALUES (?, ?, ?, ?)
    """,
        (
            datos["id_tratamiento_medicamento"],
            datos["fecha"],
            datos["hora_programada"],
            datos["estado"],
        ),
    )
    conn.commit()
    if conn is not globals().get("conexion", None):
        conn.close()


# Obtener tomas del día para todos los pacientes de un cuidador
import datetime


def obtener_tomas_del_dia(id_cuidador, fecha=None):
    """
    Obtiene todas las tomas programadas para hoy de los pacientes asociados al cuidador.
    """
    if fecha is None:
        fecha = datetime.date.today().isoformat()
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT Toma.id_toma, Toma.fecha, Toma.hora_programada, Toma.estado, 
               Paciente.nombre AS nombre_paciente, Medicamento.nombre AS nombre_medicamento
        FROM Toma
        JOIN Tratamiento_Medicamento ON Toma.id_tratamiento_medicamento = Tratamiento_Medicamento.id_tratamiento_medicamento
        JOIN Tratamiento ON Tratamiento_Medicamento.id_tratamiento = Tratamiento.id_tratamiento
        JOIN Paciente ON Tratamiento.id_paciente = Paciente.id_paciente
        JOIN Medicamento ON Tratamiento_Medicamento.id_medicamento = Medicamento.id_medicamento
        WHERE Toma.fecha = ?
          AND Paciente.id_cuidador = ?
        ORDER BY Toma.hora_programada ASC
    """
    cursor.execute(query, (fecha, id_cuidador))
    tomas = [
        dict(zip([col[0] for col in cursor.description], row))
        for row in cursor.fetchall()
    ]
    if conn is not globals().get("conexion", None):
        conn.close()
    return tomas
