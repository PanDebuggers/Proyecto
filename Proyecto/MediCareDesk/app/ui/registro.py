import tkinter as tk
from tkinter import messagebox
from app.db.conexion import get_connection

class RegistroView(tk.Frame):
    def __init__(self, master, volver_a_login, on_login_success):
        super().__init__(master, bg="#f9f9f9")
        self.master = master
        self.volver_a_login = volver_a_login
        self.on_login_success = on_login_success
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Registro de cuidador")

        contenedor = tk.Frame(self, bg="#f9f9f9")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(contenedor, text="Registro de cuidador", font=("Helvetica", 18, "bold"), bg="#f9f9f9")\
            .pack(pady=(0, 20))

        self.entries = {}

        campos = [
            ("Nombre completo", "nombre"),
            ("Relación con el paciente", "relacion"),
            ("Teléfono (opcional)", "contacto"),
            ("Correo electrónico", "email"),
            ("Contraseña", "password"),
            ("Confirmar contraseña", "confirmar_password")
        ]

        for label_text, key in campos:
            tk.Label(contenedor, text=label_text, bg="#f9f9f9", font=("Helvetica", 12, "bold"), anchor="w")\
                .pack(anchor="w", padx=10)
            show = "*" if "password" in key else ""
            entry = tk.Entry(contenedor, width=35, show=show, font=("Helvetica", 11), relief="solid", bd=1)
            entry.pack(pady=5, padx=10, ipady=3)
            self.entries[key] = entry

        # Casilla de términos
        self.acepta_terminos = tk.IntVar()
        self.check_terminos = tk.Checkbutton(
            contenedor, text="Acepto términos y condiciones", variable=self.acepta_terminos,
            command=self.toggle_boton, bg="#f9f9f9", font=("Helvetica", 10)
        )
        self.check_terminos.pack(pady=(10, 5))

        # Botón de registro
        self.btn_registrarse = tk.Button(
            contenedor, text="Registrarse", command=self.registrar, state="disabled",
            bg="#007acc", fg="white", font=("Helvetica", 12, "bold"), relief="flat", width=25
        )
        self.btn_registrarse.pack(pady=(5, 15))

        # Enlace para volver
        btn_volver = tk.Button(
            contenedor, text="¿Ya estás registrado? Inicia sesión", command=self.volver,
            fg="blue", relief="flat", bg="#f9f9f9", font=("Helvetica", 10, "underline"), cursor="hand2"
        )
        btn_volver.pack(pady=(0, 10))


    def toggle_boton(self):
        self.btn_registrarse.config(state="normal" if self.acepta_terminos.get() else "disabled")

    def registrar(self):
        nombre = self.entries["nombre"].get().strip()
        relacion = self.entries["relacion"].get().strip()
        contacto = self.entries["contacto"].get().strip() or None
        email = self.entries["email"].get().strip()
        password = self.entries["password"].get().strip()
        confirmar = self.entries["confirmar_password"].get().strip()

        if not all([nombre, relacion, email, password, confirmar]):
            messagebox.showwarning("Campos incompletos", "Por favor completa los campos obligatorios.")
            return

        if password != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Cuidador (nombre, relacion, contacto, email, password_hash)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, relacion, contacto, email, password))
            conn.commit()
            messagebox.showinfo("Registro exitoso", "Ya puedes iniciar sesión.")
            self.volver()
        except Exception:
            messagebox.showerror("Error", "Ya existe un usuario con ese correo.")
        finally:
            conn.close()

    def volver(self):
        self.destroy()
        self.volver_a_login(master=self.master, on_login_success=self.on_login_success)
