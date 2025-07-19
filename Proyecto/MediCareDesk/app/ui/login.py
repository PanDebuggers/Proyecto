import tkinter as tk
from tkinter import messagebox
from app.logic.auth import validar_credenciales, obtener_cuidador_por_email
import app.session as session
  # NUEVO: para guardar el cuidador activo

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("MediCareDesk - Iniciar Sesión")

        tk.Label(self, text="Correo electrónico").grid(row=0, column=0, pady=5, sticky="w")
        self.entry_email = tk.Entry(self, width=30)
        self.entry_email.grid(row=0, column=1, pady=5)

        tk.Label(self, text="Contraseña").grid(row=1, column=0, pady=5, sticky="w")
        self.entry_password = tk.Entry(self, width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self, text="Iniciar sesión", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        if validar_credenciales(email, password):
            session.cuidador_actual = obtener_cuidador_por_email(email)  # GUARDAMOS el cuidador activo
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.on_login_success(email)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
