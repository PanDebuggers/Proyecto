import tkinter as tk
from tkinter import messagebox
from app.db.modelos import insertar_cuidador
import os
import customtkinter as ctk

class RegistroView(tk.Frame):
    def __init__(self, master, volver_callback):
        super().__init__(master)
        self.master = master
        self.volver = volver_callback
        self.pack(fill="both", expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        container = tk.Frame(self, bg="#f0f0f0")
        container.place(relx=0.5, rely=0.5, anchor="center")

        logo_path = os.path.abspath("resources/iconos/MediCareDesk_Logo_255x255.png")
        if os.path.exists(logo_path):
            self.logo = tk.PhotoImage(file=logo_path)
            tk.Label(container, image=self.logo, bg="#f0f0f0").pack(pady=(0, 10))

        tk.Label(container, text="Registro de cuidador", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=(0, 20))

        self.campos = {}
        for label_text in [
            "Nombre completo", "Relación con el paciente",
            "Teléfono", "Correo electrónico", "Contraseña", "Confirmar contraseña"
        ]:
            tk.Label(container, text=label_text, font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")

            entry = tk.Entry(
                container,
                width=35,
                font=("Arial", 13),
                show="*" if "contraseña" in label_text.lower() else ""
            )
            entry.pack(pady=5)
            self.campos[label_text] = entry

        ctk.CTkButton(container, text="Registrarme", command=self.registrar, width=200).pack(pady=(20, 10))
        ctk.CTkButton(container, text="Volver", command=self.volver_a_login, width=200, fg_color="#cccccc", text_color="black").pack()

    def registrar(self):
        nombre = self.campos["Nombre completo"].get()
        relacion = self.campos["Relación con el paciente"].get()
        contacto = self.campos["Teléfono"].get()
        email = self.campos["Correo electrónico"].get()
        password = self.campos["Contraseña"].get()
        password2 = self.campos["Confirmar contraseña"].get()

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
