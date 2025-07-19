from app.db.modelos import buscar_cuidador_por_email
import tkinter as tk
from tkinter import Frame

class MenuLateral(Frame):
    def __init__(self, master, email_cuidador):
        super().__init__(master)

        cuidador = buscar_cuidador_por_email(email_cuidador)
        nombre_cuidador = cuidador[1] if cuidador else "Usuario"

        label_nombre = tk.Label(self, text=f"Bienvenido: {nombre_cuidador}")
        label_nombre.pack()