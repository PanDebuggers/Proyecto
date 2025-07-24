def registrar_toma(cuidador_id, medicamento_id, fecha, hora):
    """Simula el registro de una toma. Devuelve True si los datos son válidos, False si falta algún dato."""
    if cuidador_id and medicamento_id and fecha and hora:
        print(f"Toma registrada: cuidador_id={cuidador_id}, medicamento_id={medicamento_id}, fecha={fecha}, hora={hora}")
        print("Registro exitoso. Todos los datos fueron proporcionados.")
        return True
    print("Error: Faltan datos para registrar la toma.")
    print(f"Datos recibidos: cuidador_id={cuidador_id}, medicamento_id={medicamento_id}, fecha={fecha}, hora={hora}")
    return False

def obtener_tomas_por_cuidador(cuidador_id):
    """Simula la obtención de tomas para un cuidador. Devuelve una lista de diccionarios."""
    if cuidador_id:
        tomas = [
            {"id_toma": 1, "fecha": "2025-07-24", "hora_programada": "08:00", "nombre_paciente": "Juan", "nombre_medicamento": "Paracetamol", "estado": "tomada"},
            {"id_toma": 2, "fecha": "2025-07-24", "hora_programada": "12:00", "nombre_paciente": "Ana", "nombre_medicamento": "Ibuprofeno", "estado": "programada"}
        ]
        print(f"Historial de tomas para cuidador {cuidador_id}:")
        for toma in tomas:
            print(f"ID: {toma['id_toma']}, Fecha: {toma['fecha']}, Hora: {toma['hora_programada']}, Paciente: {toma['nombre_paciente']}, Medicamento: {toma['nombre_medicamento']}, Estado: {toma['estado']}")
        print(f"Total de tomas encontradas: {len(tomas)}")
        return tomas
    print("No se encontró historial de tomas para cuidador.")
    return []

def obtener_alertas_tomas(cuidador_id):
    """Simula la obtención de alertas de tomas para un cuidador. Devuelve una lista de alertas."""
    if cuidador_id:
        alertas = [
            {"id_toma": 2, "alerta": "Toma programada para las 12:00"},
            {"id_toma": 1, "alerta": "Toma tomada a las 08:00"}
        ]
        print(f"Alertas de tomas para cuidador {cuidador_id}:")
        for alerta in alertas:
            print(f"ID: {alerta['id_toma']}, Mensaje: {alerta['alerta']}")
        print(f"Total de alertas encontradas: {len(alertas)}")
        return alertas
    print("No se encontraron alertas de tomas para cuidador.")
    return []
