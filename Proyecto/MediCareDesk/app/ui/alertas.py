import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from app.db import modelos


def mostrar_alertas_semanales(frame, id_cuidador):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(
        frame,
        text="Alertas: Próxima toma semanal por paciente",
        font=("Arial", 18, "bold"),
        bg="#f0f0f0",
    ).pack(pady=10)

    columnas = ("Paciente", "Fecha", "Hora", "Medicamento", "Estado", "Alerta")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    estados_colores = {
        "programada": "#FFFACD",
        "tomada": "#C1FFC1",
        "omitida": "#FFB6B6",
        "pendiente": "#E0E0E0",
    }

    tomas = modelos.obtener_proximas_tomas_semanales_por_paciente(id_cuidador)
    for toma in tomas:
        color = estados_colores.get(toma["estado"], "white")
        alerta_txt = "Atrasada" if toma.get("alerta_tipo") == "atrasada" else "Próxima"
        tabla.insert(
            "",
            "end",
            values=(
                toma["nombre_paciente"],
                toma["fecha"],
                toma["hora_programada"],
                toma["nombre_medicamento"],
                toma["estado"].capitalize(),
                alerta_txt,
            ),
            tags=(toma["estado"], alerta_txt),
        )
        tabla.tag_configure(toma["estado"], background=color)
        if alerta_txt == "Atrasada":
            tabla.tag_configure("Atrasada", foreground="red", font=("Arial", 12, "bold"))
        else:
            tabla.tag_configure("Próxima", foreground="black")

    if not tomas:
        tk.Label(
            frame, text="No hay próximas tomas programadas para esta semana.", fg="gray"
        ).pack(pady=10)


# Alias para compatibilidad con el menú lateral y base_view
def mostrar_alertas(frame, id_cuidador):
    mostrar_alertas_semanales(frame, id_cuidador)
