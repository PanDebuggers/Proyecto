import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from app.db import modelos


def mostrar_historial_tomas(frame, id_paciente, nombre_paciente=None):
    for widget in frame.winfo_children():
        widget.destroy()

    titulo = f"Historial de Tomas"
    if nombre_paciente:
        titulo += f" - {nombre_paciente}"
    tk.Label(frame, text=titulo, font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    columnas = ("Fecha", "Hora", "Medicamento", "Estado", "Verificada")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=16)
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

    tomas = modelos.obtener_historial_tomas_paciente(id_paciente)
    for toma in tomas:
        color = estados_colores.get(toma["estado"], "white")
        verificada_str = "Sí" if toma.get("verificada", 0) else "No"
        tabla.insert(
            "",
            "end",
            values=(
                toma["fecha"],
                toma["hora_programada"],
                toma["nombre_medicamento"],
                toma["estado"].capitalize(),
                verificada_str,
            ),
            tags=(toma["estado"],),
        )
        tabla.tag_configure(toma["estado"], background=color)

    if not tomas:
        tk.Label(
            frame,
            text="No hay tomas registradas para este paciente.",
            bg="#f0f0f0",
            fg="gray",
        ).pack(pady=20)
