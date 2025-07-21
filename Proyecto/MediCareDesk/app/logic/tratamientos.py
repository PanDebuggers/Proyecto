# Generar tomas programadas para un tratamiento-medicamento
def generar_tomas_tratamiento(asignacion_id):
    '''
    Genera las tomas programadas para el tratamiento-medicamento asignado,
    según la frecuencia y el rango de fechas.
    '''
    from app.db import modelos
    import datetime
    asignacion = modelos.obtener_tratamiento_medicamento(asignacion_id)
    print(f"[DEBUG] Asignación recuperada: {asignacion}")
    if not asignacion:
        print("[DEBUG] No se encontró la asignación.")
        return
    fecha_inicio = asignacion['fecha_inicio']
    fecha_fin = asignacion['fecha_fin']
    frecuencia = asignacion['frecuencia']
    hora_base = '08:00'  # Hora base por defecto
    if not fecha_inicio or not fecha_fin:
        print(f"[DEBUG] Fechas inválidas: inicio={fecha_inicio}, fin={fecha_fin}")
        return
    fecha_ini = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
    dias = (fecha_fin_dt - fecha_ini).days + 1
    print(f"[DEBUG] Generando tomas para {dias} días, frecuencia: {frecuencia}")
    for i in range(dias):
        fecha = (fecha_ini + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        if frecuencia == 'una_vez_al_dia':
            horas = [hora_base]
        elif frecuencia == 'cada_8_horas':
            horas = ['08:00', '16:00', '00:00']
        elif frecuencia == 'cada_12_horas':
            horas = ['08:00', '20:00']
        elif frecuencia == 'cada_24_horas':
            horas = [hora_base]
        else:
            horas = [hora_base]
        for hora in horas:
            print(f"[DEBUG] Creando toma para fecha={fecha}, hora={hora}")
            modelos.crear_toma({
                'id_tratamiento_medicamento': asignacion_id,
                'fecha': fecha,
                'hora_programada': hora,
                'estado': 'programada'
            })
from datetime import datetime, timedelta
from app.db import modelos
import re


def asignar_medicamento_a_tratamiento(**kwargs):
    """Versión mejorada con validación robusta de hora"""
    required_fields = ['id_tratamiento', 'id_medicamento', 'frecuencia', 'via_administracion', 'estado']
    # Verificar campos obligatorios
    missing = [field for field in required_fields if field not in kwargs or not kwargs[field]]
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")

    # Obtener tratamiento
    tratamiento = modelos.obtener_tratamiento(kwargs['id_tratamiento'])
    if not tratamiento:
        raise ValueError("Tratamiento no encontrado")

    # Obtener medicamento
    medicamento = modelos.obtener_medicamento(kwargs['id_medicamento'])
    if not medicamento:
        raise ValueError("Medicamento no encontrado")

    # Establecer fechas por defecto
    kwargs.setdefault('fecha_inicio', tratamiento['fecha_inicio'])
    kwargs.setdefault('fecha_fin', tratamiento['fecha_fin'])

    # Validar fechas si se proporcionan
    if 'fecha_inicio' in kwargs and 'fecha_fin' in kwargs:
        try:
            fecha_inicio = datetime.strptime(kwargs['fecha_inicio'], '%Y-%m-%d')
            fecha_fin = datetime.strptime(kwargs['fecha_fin'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("Formato de fecha inválido")
        if fecha_fin < fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")

    # Eliminar toda lógica de hora_preferida
    if 'hora_preferida' in kwargs:
        kwargs.pop('hora_preferida')

    try:
        return modelos.crear_tratamiento_medicamento(kwargs)
    except Exception as e:
        raise ValueError(f"Error al asignar medicamento: {str(e)}")


