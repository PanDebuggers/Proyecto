from datetime import datetime, timedelta
from app.db import modelos
import re


def asignar_medicamento_a_tratamiento(**kwargs):
    """Versión mejorada con validación robusta de hora"""
    required_fields = ['id_tratamiento', 'id_medicamento', 'frecuencia', 
                      'via_administracion', 'estado', 'hora_preferida']
    
    # Verificar campos obligatorios
    missing = [field for field in required_fields if field not in kwargs or not kwargs[field]]
    if missing:
        raise ValueError(f"Faltan campos obligatorios: {', '.join(missing)}")
    
    # Validar formato de hora_preferida con regex
    hora = kwargs['hora_preferida']
    if not re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', hora):
        raise ValueError("Formato de hora inválido. Use HH:MM (24 horas)")
    
    # Validar valores de hora
    try:
        horas, minutos = map(int, hora.split(':'))
        if not (0 <= horas <= 23 and 0 <= minutos <= 59):
            raise ValueError
    except (ValueError, TypeError):
        raise ValueError("Hora inválida. Horas deben ser 00-23, minutos 00-59")
    
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
    
    try:
        return modelos.crear_tratamiento_medicamento(kwargs)
    except Exception as e:
        raise ValueError(f"Error al asignar medicamento: {str(e)}")



##
def generar_tomas_tratamiento(asignacion_id):
    """Versión corregida con mejor manejo de fechas"""
    asignacion = modelos.obtener_tratamiento_medicamento(asignacion_id)
    if not asignacion:
        raise ValueError("Asignación no encontrada")
    
    tratamiento = modelos.obtener_tratamiento(asignacion['id_tratamiento'])
    if not tratamiento:
        raise ValueError("Tratamiento no encontrado")
    
    # Convertir fechas a objetos date
    from datetime import datetime, timedelta
    
    fecha_inicio = datetime.strptime(asignacion.get('fecha_inicio') or tratamiento['fecha_inicio'], '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(asignacion.get('fecha_fin') or tratamiento['fecha_fin'], '%Y-%m-%d').date()
    
    # Resto de la lógica de generación de tomas...
    
    hora_preferida = datetime.strptime(asignacion['hora_preferida'], '%H:%M').time()
    
    frecuencia_map = {
        'una_vez_al_dia': timedelta(days=1),
        'cada_8_horas': timedelta(hours=8),
        'cada_12_horas': timedelta(hours=12),
        'cada_24_horas': timedelta(days=1)
    }
    
    frecuencia = frecuencia_map.get(asignacion['frecuencia'], timedelta(days=1))
    
    fecha_actual = datetime.combine(fecha_inicio, hora_preferida)
    
    while fecha_actual.date() <= fecha_fin:
        modelos.crear_toma({
            'id_tratamiento_medicamento': asignacion_id,
            'fecha': fecha_actual.strftime('%Y-%m-%d'),
            'hora_programada': fecha_actual.strftime('%H:%M:%S'),
            'estado': 'programada'
        })
        
        fecha_actual += frecuencia