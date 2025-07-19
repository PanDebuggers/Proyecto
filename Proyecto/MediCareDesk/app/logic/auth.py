from app.db.modelos import (
    buscar_cuidador_por_credenciales,
    buscar_cuidador_por_email
)

def validar_credenciales(email, password):
    return buscar_cuidador_por_credenciales(email, password) is not None

def obtener_cuidador_por_email(email):
    return buscar_cuidador_por_email(email)
