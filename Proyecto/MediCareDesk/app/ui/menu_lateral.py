import tkinter as tk
from app import session

class MenuLateral(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.mostrar_usuario()

    def mostrar_usuario(self):
        cuidador = session.cuidador_actual
        if cuidador:
            nombre = cuidador["nombre"]
            label_usuario = tk.Label(self, text=f"Cuidador: {nombre}")
            label_usuario.pack(pady=5)
