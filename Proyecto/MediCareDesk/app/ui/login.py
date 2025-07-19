import tkinter as tk
from tkinter import messagebox
from app.logic.auth import validar_credenciales, obtener_cuidador_por_email
from app import session

class LoginView(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, bg="#f9f9f9")
        self.master = master
        self.on_login_success = on_login_success
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        self.master.title("MediCareDesk - Iniciar Sesión")

        contenedor = tk.Frame(self, bg="#f9f9f9")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(contenedor, text="Iniciar sesión", font=("Helvetica", 18, "bold"), bg="#f9f9f9")\
            .pack(pady=(0, 20))

        self.entries = {}

        campos = [
            ("Correo electrónico", "email"),
            ("Contraseña", "password")
        ]

        for label_text, key in campos:
            tk.Label(contenedor, text=label_text, bg="#f9f9f9", font=("Helvetica", 12, "bold"), anchor="w")\
                .pack(anchor="w", padx=10)
            show = "*" if "password" in key else ""
            entry = tk.Entry(contenedor, width=35, show=show, font=("Helvetica", 11), relief="solid", bd=1)
            entry.pack(pady=5, padx=10, ipady=3)
            self.entries[key] = entry

        # Botón de login
        self.login_button = tk.Button(
            contenedor, text="Iniciar sesión", command=self.login,
            bg="#007acc", fg="white", font=("Helvetica", 12, "bold"), relief="flat", width=25
        )
        self.login_button.pack(pady=(15, 10))

        # Enlace para registrarse
        self.register_button = tk.Button(
            contenedor, text="¿No tienes cuenta? Regístrate aquí", command=self.abrir_registro,
            fg="blue", relief="flat", bg="#f9f9f9", font=("Helvetica", 10, "underline"), cursor="hand2"
        )
        self.register_button.pack()

    def login(self):
        email = self.entries["email"].get().strip()
        password = self.entries["password"].get().strip()

        if validar_credenciales(email, password):
            session.cuidador_actual = obtener_cuidador_por_email(email)
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            self.on_login_success(email)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_registro(self):
        from app.ui.registro import RegistroView
        self.destroy()
        RegistroView(master=self.master, volver_a_login=self.__class__, on_login_success=self.on_login_success)
