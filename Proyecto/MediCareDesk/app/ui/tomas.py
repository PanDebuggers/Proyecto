# Vista para mostrar las tomas del día
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from app.db import modelos


def mostrar_tomas_dia(frame, id_cuidador):
    import datetime
    from tkinter import messagebox
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Mostrar todas las tomas programadas de la semana (lista cronológica)
    tomas = modelos.obtener_tomas_semana_por_cuidador(id_cuidador)

    tk.Label(frame, text="Tomas de la semana", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

    columnas = ("Fecha", "Hora", "Paciente", "Medicamento", "Estado")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=16)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    estados_colores = {
        "programada": "#FFFACD",  # Amarillo claro
        "tomada": "#C1FFC1",      # Verde claro
        "omitida": "#FFB6B6",     # Rojo claro
        "pendiente": "#E0E0E0"    # Gris claro
    }

    for toma in tomas:
        color = estados_colores.get(toma["estado"], "white")
        tabla.insert("", "end", values=(
            toma["fecha"],
            toma["hora_programada"],
            toma["nombre_paciente"],
            toma["nombre_medicamento"],
            toma["estado"].capitalize()
        ), tags=(toma["estado"],))
        tabla.tag_configure(toma["estado"], background=color)

    if not tomas:
        tk.Label(frame, text="No hay tomas programadas para esta semana.", fg="gray").pack(pady=10)

    # Botones para marcar como tomada u omitida
    def marcar_toma(estado):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selecciona una toma", "Por favor selecciona una toma de la lista.")
            return
        item = seleccion[0]
        id_toma = tabla.item(item, "values")[0]
        modelos.actualizar_estado_toma(id_toma, estado)
        mostrar_tomas_dia(frame, id_cuidador)  # Refrescar la vista

    btn_frame = tk.Frame(frame, bg="#f0f0f0")
    btn_frame.pack(pady=10)
    btn_tomada = ctk.CTkButton(btn_frame, text="Marcar como Tomada", command=lambda: marcar_toma("tomada"), fg_color="#90EE90")
    btn_tomada.pack(side="left", padx=10)
    btn_omitida = ctk.CTkButton(btn_frame, text="Marcar como Omitida", command=lambda: marcar_toma("omitida"), fg_color="#FF6347")
    btn_omitida.pack(side="left", padx=10)

    # ...existing code...
