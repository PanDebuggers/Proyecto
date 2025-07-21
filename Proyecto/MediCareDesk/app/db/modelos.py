from .conexion import obtener_conexion

def obtener_conexion():
    import sqlite3
    # Si existe la conexión global, úsala
    if 'conexion' in globals() and globals()['conexion'] is not None:
        return globals()['conexion']
    # Si no, crea una nueva (para producción)
    return sqlite3.connect("MediCareDesk.db")

def insertar_cuidador(nombre, relacion, contacto, email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, relacion, contacto, email, password_hash))
    conn.commit()
    if conn is not globals().get('conexion', None):
        conn.close()

def obtener_pacientes(activos=True):
    """Obtiene todos los pacientes (solo activos por defecto)"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = "SELECT * FROM Paciente"
    if activos:
        query += " WHERE activo = 1"
    cursor.execute(query)
    pacientes = [dict(paciente) for paciente in cursor.fetchall()]
    if conn is not globals().get('conexion', None):
        conn.close()
    return pacientes



def obtener_medicamento(medicamento_id):
    """Obtiene un medicamento específico por ID"""
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicamento WHERE id_medicamento = ?", (medicamento_id,))
        resultado = cursor.fetchone()
        return dict(resultado) if resultado else None
    finally:
        if conn is not globals().get('conexion', None):
            conn.close()

def obtener_medicamentos():
    """Obtiene todos los medicamentos"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Medicamento")
    medicamentos = [dict(med) for med in cursor.fetchall()]
    if conn is not globals().get('conexion', None):
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
    if conn is not globals().get('conexion', None):
        conn.close()
    return tratamientos

def crear_tratamiento(datos):
    """Crea un nuevo tratamiento"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Tratamiento (id_paciente, nombre_tratamiento, descripcion, 
                               estado, fecha_inicio, fecha_fin)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datos['id_paciente'],
        datos['nombre_tratamiento'],
        datos.get('descripcion', ''),
        datos['estado'],
        datos['fecha_inicio'],
        datos['fecha_fin']
    ))
    conn.commit()
    tratamiento_id = cursor.lastrowid
    if conn is not globals().get('conexion', None):
        conn.close()
    return tratamiento_id

def obtener_tratamiento(tratamiento_id):
    """Obtiene un tratamiento específico por ID"""
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tratamiento WHERE id_tratamiento = ?", (tratamiento_id,))
        resultado = cursor.fetchone()
        if resultado:
            # Convertir a diccionario y asegurar los tipos de fecha
            tratamiento = dict(resultado)
            tratamiento['fecha_inicio'] = str(tratamiento['fecha_inicio'])  # Asegurar string
            tratamiento['fecha_fin'] = str(tratamiento['fecha_fin'])      # Asegurar string
            return tratamiento
        return None
    finally:
        if conn is not globals().get('conexion', None):
            conn.close()


def crear_tratamiento_medicamento(datos):
    """Crea una nueva asignación tratamiento-medicamento"""
    conn = obtener_conexion()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Tratamiento_Medicamento (
                    id_tratamiento, id_medicamento, dosis, frecuencia, 
                    via_administracion, fecha_inicio, fecha_fin, estado, hora_preferida
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datos['id_tratamiento'],
                datos['id_medicamento'],
                datos.get('dosis', ''),
                datos['frecuencia'],
                datos['via_administracion'],
                datos.get('fecha_inicio'),
                datos.get('fecha_fin'),
                datos['estado'],
                datos['hora_preferida']
            ))
            return cursor.lastrowid
    finally:
        if conn is not globals().get('conexion', None):
            conn.close()

def obtener_tratamiento_medicamento(asignacion_id):
    """Obtiene una asignación tratamiento-medicamento por ID"""
    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Tratamiento_Medicamento 
            WHERE id_tratamiento_medicamento = ?
        """, (asignacion_id,))
        resultado = cursor.fetchone()
        if resultado:
            asignacion = dict(resultado)
            # Convertir fechas a string si existen
            if asignacion.get('fecha_inicio'):
                asignacion['fecha_inicio'] = str(asignacion['fecha_inicio'])
            if asignacion.get('fecha_fin'):
                asignacion['fecha_fin'] = str(asignacion['fecha_fin'])
            return asignacion
        return None
    finally:
        if conn is not globals().get('conexion', None):
            conn.close()

def crear_toma(datos):
    """Crea una nueva toma programada"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Toma (id_tratamiento_medicamento, fecha, hora_programada, estado)
        VALUES (?, ?, ?, ?)
    """, (
        datos['id_tratamiento_medicamento'],
        datos['fecha'],
        datos['hora_programada'],
        datos['estado']
    ))
    conn.commit()
    if conn is not globals().get('conexion', None):
        conn.close()


def buscar_cuidador_por_email(email):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4]
        }
        return cuidador
    return None

def buscar_cuidador_por_credenciales(email, password_hash):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cuidador, nombre, relacion, contacto, email FROM Cuidador WHERE email = ? AND password_hash = ?", (email, password_hash))
    row = cursor.fetchone()
    conn.close()
    if row:
        cuidador = {
            "id_cuidador": row[0],
            "nombre": row[1],
            "relacion": row[2],
            "contacto": row[3],
            "email": row[4]
        }
        return cuidador
    return None
# ----------------------------------------------------------------------------------------