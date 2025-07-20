import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.logic.auth import validar_credenciales, obtener_cuidador_por_email
from app.ui.registro import RegistroView
from app import session


class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack(fill="both", expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        container = tk.Frame(self, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor="center")

        logo_path = os.path.abspath("resources/iconos/MediCareDesk_Logo_255x255.png")
        if os.path.exists(logo_path):
            self.logo = tk.PhotoImage(file=logo_path)
            tk.Label(container, image=self.logo, bg="#f0f0f0").pack(pady=(0, 15))

        tk.Label(container, text="Iniciar sesión", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        self.email_entry = tk.Entry(container, width=35, font=("Arial", 13))
        self.password_entry = tk.Entry(container, width=35, show="*", font=("Arial", 13))

        for label, entry in [("Correo electrónico", self.email_entry), ("Contraseña", self.password_entry)]:
            tk.Label(container, text=label, font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
            entry.pack(pady=5)

        ctk.CTkButton(container, text="Iniciar sesión", command=self.iniciar_sesion, width=200).pack(pady=(20, 10))
        ctk.CTkButton(container, text="Registrarse", command=self.abrir_registro, width=200, fg_color="#cccccc", text_color="black").pack()

    def iniciar_sesion(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if validar_credenciales(email, password):
            # ✅ Obtener datos completos del cuidador
            cuidador = obtener_cuidador_por_email(email)
            session.cuidador_actual = cuidador
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso para {email}")
            # ✅ Pasar cuidador completo, no solo el email
            self.on_login_success(cuidador)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_registro(self):
        self.destroy()
        RegistroView(self.master, volver_callback=self.volver_login)

    def volver_login(self):
        self.destroy()
        LoginView(self.master, on_login_success=self.on_login_success)
