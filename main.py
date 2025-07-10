import tkinter as tk
from tkinter import messagebox
# import mysql.connector  # Desactivado mientras no tienes BD

# Configuración de conexión (no usada por ahora)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'medicare_desk'
}

def limpiar_ventana(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def registrar_paciente(ventana):
    limpiar_ventana(ventana)

    tk.Label(ventana, text="Registro de Paciente", font=("Arial", 16, "bold")).pack(pady=10)

    campos = {
        "Nombre": tk.StringVar(),
        "Edad": tk.StringVar(),
        "Género": tk.StringVar(),
        "Identificación": tk.StringVar(),
        "Contacto de emergencia": tk.StringVar(),
        "Observaciones médicas": tk.StringVar()
    }

    entradas = {}

    for campo, var in campos.items():
        tk.Label(ventana, text=campo, font=("Arial", 12)).pack()
        entrada = tk.Entry(ventana, textvariable=var, font=("Arial", 12), width=40)
        entrada.pack(pady=3)
        entradas[campo] = entrada

    def guardar():
        datos = {campo: var.get() for campo, var in campos.items()}
        if not datos["Nombre"] or not datos["Identificación"]:
            messagebox.showerror("Error", "Los campos Nombre e Identificación son obligatorios.")
            return

        # Simulación de guardado (sin base de datos)
        messagebox.showinfo("DEBUG", f"Paciente capturado:\n\n{datos}")
        iniciar_app(ventana)

    tk.Button(ventana, text="Guardar", command=guardar, bg="#2ecc71", fg="white", font=("Arial", 12), width=15).pack(pady=10)
    tk.Button(ventana, text="Volver", command=lambda: iniciar_app(ventana), bg="#95a5a6", font=("Arial", 12), width=15).pack(pady=5)

def iniciar_app(ventana=None):
    if ventana is None:
        ventana = tk.Tk()

    ventana.title("MediCareDesk - Sistema de Seguimiento de Medicación")
    ventana.geometry("600x600")
    ventana.configure(bg="#f0f0f0")
    limpiar_ventana(ventana)

    tk.Label(ventana, text="Bienvenido a MediCareDesk", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(ventana, text="Seleccione una opción para comenzar", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

    botones = [
        ("Registrar paciente", lambda: registrar_paciente(ventana)),
        ("Agregar medicamento", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Programar toma", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Verificar toma realizada", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Marcar toma como omitida", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Consultar historial", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Generar reporte", lambda: messagebox.showinfo("Módulo", "Funcionalidad pendiente")),
        ("Salir", ventana.quit)
    ]

    for texto, comando in botones:
        tk.Button(ventana, text=texto, command=comando,
                  bg="#3498db" if texto != "Salir" else "#c0392b",
                  fg="white", font=("Arial", 12), width=30, height=2).pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    print("Iniciando MediCareDesk...")
    iniciar_app()
