import tkinter as tk
from tkinter import messagebox
from app.db.modelos import insertar_cuidador

class RegistroView(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master)
        self.master = master
        self.volver = volver_callback
        self.pack()
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self, text="Registro de cuidador", font=("Helvetica", 16)).pack(pady=10)

        self.nombre = tk.Entry(self)
        self.relacion = tk.Entry(self)
        self.contacto = tk.Entry(self)
        self.email = tk.Entry(self)
        self.password = tk.Entry(self, show="*")
        self.confirmar_password = tk.Entry(self, show="*")

        for label, entry in [
            ("Nombre completo", self.nombre),
            ("Relación con el paciente", self.relacion),
            ("Teléfono", self.contacto),
            ("Correo electrónico", self.email),
            ("Contraseña", self.password),
            ("Confirmar contraseña", self.confirmar_password)
        ]:
            tk.Label(self, text=label).pack()
            entry.pack()

        tk.Button(self, text="Registrarme", command=self.registrar).pack(pady=10)
        tk.Button(self, text="Volver", command=self.volver_a_login).pack()

    def registrar(self):
        nombre = self.nombre.get()
        relacion = self.relacion.get()
        contacto = self.contacto.get()
        email = self.email.get()
        password = self.password.get()
        password2 = self.confirmar_password.get()

        if not all([nombre, relacion, contacto, email, password, password2]):
            messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
            return

        if password != password2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        try:
            insertar_cuidador(nombre, relacion, contacto, email, password)
            messagebox.showinfo("Registro exitoso", "Ya puedes iniciar sesión.")
            self.volver_a_login()
        except Exception:
            messagebox.showerror("Error", "Ya existe un usuario con ese correo.")

    def volver_a_login(self):
        self.destroy()
        self.volver()
