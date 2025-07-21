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


