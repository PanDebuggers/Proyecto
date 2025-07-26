import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class MedicamentosManager:
    def __init__(self, frame_dinamico):
        self.frame_dinamico = frame_dinamico
        self.tree = None
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_FILENAME = os.path.join(self.BASE_DIR, "..", "..", "data", "MediCareDesk.db")
        self.setup_ui()
        
    def setup_ui(self):
        # Limpiar frame dinámico
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()

        # Frame principal con scroll
        main_frame = tk.Frame(self.frame_dinamico, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

        # CORRECCIÓN PRINCIPAL: Paréntesis correctamente balanceados
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        lbl = tk.Label(
            scrollable_frame,
            text="Gestión de Medicamentos",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
        )
        lbl.pack(pady=(10, 20))

        # Crear tabla Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        columnas = (
            "ID", "Nombre", "Principio Activo", "Presentación",
            "Laboratorio", "Caducidad", "Registro"
        )

        self.tree = ttk.Treeview(
            scrollable_frame, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150, anchor="w")
        self.tree.column("Principio Activo", width=150, anchor="w")
        self.tree.column("Presentación", width=120, anchor="center")
        self.tree.column("Laboratorio", width=120, anchor="w")
        self.tree.column("Caducidad", width=100, anchor="center")
        self.tree.column("Registro", width=120, anchor="center")

        for col in columnas:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Botones de acción
        btn_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        btn_agregar = ctk.CTkButton(
            btn_frame, text="Agregar Medicamento", command=self.agregar_medicamento)
        btn_agregar.pack(side=tk.LEFT, padx=5)

        btn_editar = ctk.CTkButton(
            btn_frame, text="Editar Medicamento", command=self.editar_medicamento)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = ctk.CTkButton(
            btn_frame,
            text="Eliminar Medicamento",
            command=self.eliminar_medicamento,
            fg_color="#d9534f",
            hover_color="#c9302c",
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        btn_refresh = ctk.CTkButton(btn_frame, text="Refrescar", command=self.cargar_datos)
        btn_refresh.pack(side=tk.LEFT, padx=5)

        # Cargar datos iniciales
        self.cargar_datos()
    
    # Resto de los métodos permanecen exactamente iguales
    # (cargar_datos, agregar_medicamento, editar_medicamento, eliminar_medicamento)
    # ...

def mostrar_medicamentos(frame_dinamico):
    manager = MedicamentosManager(frame_dinamico)