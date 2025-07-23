import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from app.db import modelos

def mostrar_historial_todas_tomas_cuidador(frame, id_cuidador):
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Historial de Tomas de Todos los Pacientes", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    columnas = ("Paciente", "Fecha", "Hora", "Medicamento", "Estado")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=20)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    estados_colores = {
        "programada": "#FFD700",
        "tomada": "#90EE90",
        "omitida": "#FF6347",
        "pendiente": "#D3D3D3",
    }

    pacientes = modelos.obtener_pacientes(id_cuidador=id_cuidador)
    print(f"[DEBUG] Pacientes del cuidador {id_cuidador}: {[p['nombre'] for p in pacientes]}")
    for paciente in pacientes:
        tomas = modelos.obtener_historial_tomas_paciente(paciente["id_paciente"])
        print(f"[DEBUG] Tomas de paciente {paciente['nombre']} ({paciente['id_paciente']}): {tomas}")
        for toma in tomas:
            if toma["estado"] in ("omitida", "tomada"):
                color = estados_colores.get(toma["estado"], "white")
                tabla.insert(
                    "",
                    "end",
                    values=(
                        paciente["nombre"],
                        toma["fecha"],
                        toma["hora_programada"],
                        toma["nombre_medicamento"],
                        toma["estado"].capitalize(),
                    ),
                    tags=(toma["estado"],),
                )
                tabla.tag_configure(toma["estado"], background=color)

    if not tabla.get_children():
        tk.Label(frame, text="No hay tomas omitidas ni tomadas registradas.", fg="gray").pack(pady=10)
