import tkinter as tk
from tkinter import messagebox
from app.logic.auth import validar_credenciales, obtener_cuidador_por_email
from app.ui.registro import RegistroView
from app import session

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack()
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self, text="Iniciar sesión", font=("Helvetica", 16)).pack(pady=10)

        self.email_entry = tk.Entry(self, width=30)
        self.password_entry = tk.Entry(self, width=30, show="*")

        for label, entry in [("Correo electrónico", self.email_entry), ("Contraseña", self.password_entry)]:
            tk.Label(self, text=label).pack()
            entry.pack()

        tk.Button(self, text="Iniciar sesión", command=self.iniciar_sesion).pack(pady=10)
        tk.Button(self, text="Registrarse", command=self.abrir_registro).pack()

    def iniciar_sesion(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if validar_credenciales(email, password):
            session.cuidador_actual = obtener_cuidador_por_email(email)
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso para {email}")
            self.on_login_success(email)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_registro(self):
        self.destroy()
        RegistroView(self.master, volver_callback=self.volver_login)

    def volver_login(self):
        self.destroy()
        LoginView(self.master, on_login_success=self.on_login_success)
