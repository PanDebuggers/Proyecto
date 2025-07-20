import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import sqlite3
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def mostrar_pacientes(frame_dinamico, id_cuidador):
    # Configuración inicial
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_FILENAME = os.path.join(BASE_DIR, "..", "..", "data", "MediCareDesk.db")
    
    # Limpiar frame dinámico
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    # Frame principal con mejor organización
    main_frame = ctk.CTkFrame(frame_dinamico)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Título con estilo mejorado
    title_frame = ctk.CTkFrame(main_frame, corner_radius=0)
    title_frame.pack(fill="x", pady=(0, 10))
    
    lbl = ctk.CTkLabel(title_frame, text="Gestión de Pacientes", 
                      font=("Helvetica", 18, "bold"))
    lbl.pack(pady=10)

    # Frame para la tabla con scrollbar
    table_frame = ctk.CTkFrame(main_frame)
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Scrollbar
    scrollbar = ttk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    # Configuración de estilo para la tabla
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", 
                  background="#ffffff",
                  foreground="#333333",
                  rowheight=30,
                  fieldbackground="#ffffff",
                  borderwidth=0,
                  font=('Helvetica', 10))
    style.configure("Treeview.Heading", 
                  font=('Helvetica', 10, 'bold'),
                  background="#4b8aeb",
                  foreground="white",
                  borderwidth=0)
    style.map("Treeview.Heading", background=[('active', '#3a6ebd')])

    # Crear tabla Treeview con mejor configuración
    columnas = (
        "ID", "Nombre", "Edad", "Género",
        "Contacto Emergencia", "Estado",
        "Tratamientos Totales", "Tratamientos Activos"
    )

    tree = ttk.Treeview(table_frame, columns=columnas, show="headings",
                       yscrollcommand=scrollbar.set, selectmode="browse")
    
    # Configurar columnas
    tree.column("ID", width=50, anchor="center", stretch=False)
    tree.column("Nombre", width=180, anchor="w")
    tree.column("Edad", width=60, anchor="center", stretch=False)
    tree.column("Género", width=80, anchor="center", stretch=False)
    tree.column("Contacto Emergencia", width=180, anchor="w")
    tree.column("Estado", width=80, anchor="center", stretch=False)
    tree.column("Tratamientos Totales", width=120, anchor="center", stretch=False)
    tree.column("Tratamientos Activos", width=120, anchor="center", stretch=False)

    for col in columnas:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=5, pady=5)
    scrollbar.config(command=tree.yview)

    # Función para cargar datos con manejo de errores mejorado
    def cargar_datos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    id_paciente, nombre, edad, genero,
                    contacto_emergencia, 
                    CASE WHEN activo = 1 THEN 'Activo' ELSE 'Inactivo' END as estado,
                    tratamientos_totales, tratamientos_activos
                FROM Vista_Pacientes
                WHERE id_cuidador = ?
                ORDER BY nombre
            """, (id_cuidador,))
            
            pacientes = cursor.fetchall()
            
            # Insertar datos con colores alternados
            for i, paciente in enumerate(pacientes):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                tree.insert("", "end", values=paciente, tags=tags)
            
            # Configurar colores alternos
            tree.tag_configure('evenrow', background='#ffffff')
            tree.tag_configure('oddrow', background='#f5f5f5')
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", 
                               f"No se pudieron cargar los pacientes:\n{str(e)}")

    # Función para agregar paciente con validación mejorada
    def agregar_paciente():
        form = ctk.CTkToplevel()
        form.title("Agregar Nuevo Paciente")
        form.geometry("500x550")
        form.resizable(False, False)
        
        # Frame para el formulario
        form_frame = ctk.CTkFrame(form)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Variables para los campos
        nombre_var = tk.StringVar()
        edad_var = tk.StringVar()
        genero_var = tk.StringVar(value="M")
        contacto_var = tk.StringVar()
        observaciones_var = tk.StringVar()
        
        # Campos del formulario
        ctk.CTkLabel(form_frame, text="Nombre completo:").pack(pady=(10, 0))
        nombre_entry = ctk.CTkEntry(form_frame, textvariable=nombre_var)
        nombre_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Edad:").pack(pady=(0, 0))
        edad_entry = ctk.CTkEntry(form_frame, textvariable=edad_var)
        edad_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Género:").pack(pady=(0, 0))
        genero_menu = ctk.CTkOptionMenu(form_frame, values=["M", "F", "Otro"], 
                                       variable=genero_var)
        genero_menu.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Contacto de emergencia:").pack(pady=(0, 0))
        contacto_entry = ctk.CTkEntry(form_frame, textvariable=contacto_var)
        contacto_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Observaciones:").pack(pady=(0, 0))
        observaciones_entry = ctk.CTkTextbox(form_frame, height=100)
        observaciones_entry.pack(fill="x", padx=10, pady=(0, 20))
        
        # Función para guardar con validación mejorada
        def guardar_paciente():
            nombre = nombre_var.get().strip()
            edad = edad_var.get().strip()
            genero = genero_var.get()
            contacto = contacto_var.get().strip()
            observaciones = observaciones_entry.get("1.0", tk.END).strip()
            
            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre del paciente es obligatorio.")
                return
                
            if not edad.isdigit() or not (0 < int(edad) < 120):
                messagebox.showerror("Error", "La edad debe ser un número válido entre 1 y 119.")
                return
                
            if not contacto:
                messagebox.showerror("Error", "El contacto de emergencia es obligatorio.")
                return
                
            try:
                conn = sqlite3.connect(DB_FILENAME)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO Paciente (nombre, edad, genero, contacto_emergencia, observaciones)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, int(edad), genero, contacto, observaciones))

                id_paciente = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO Cuidador_Paciente (id_cuidador, id_paciente)
                    VALUES (?, ?)
                """, (id_cuidador, id_paciente))

                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Paciente agregado y asignado correctamente.")
                form.destroy()
                cargar_datos()
                
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al guardar el paciente:\n{str(e)}")
        
        # Botones
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        guardar_btn = ctk.CTkButton(btn_frame, text="Guardar Paciente", 
                                   command=guardar_paciente)
        guardar_btn.pack(side="right", padx=5)
        
        cancelar_btn = ctk.CTkButton(btn_frame, text="Cancelar", 
                                    command=form.destroy, fg_color="gray")
        cancelar_btn.pack(side="right", padx=5)
        
        # Enfocar el primer campo
        nombre_entry.focus_set()

    # Función para eliminar paciente con confirmación
    def eliminar_paciente():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un paciente para eliminar.")
            return

        paciente_data = tree.item(selected_item, "values")
        paciente_id = paciente_data[0]
        paciente_nombre = paciente_data[1]

        # Confirmación antes de eliminar
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar al paciente '{paciente_nombre}' (ID: {paciente_id})?\n\n"
            "Esta acción desvinculará al paciente de su cuenta."
        )
        
        if not confirmar:
            return

        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()

            # Verificar si el paciente tiene tratamientos activos
            cursor.execute("""
                SELECT COUNT(*) FROM Tratamiento 
                WHERE id_paciente = ? AND estado = 'activo'
            """, (paciente_id,))
            
            tratamientos_activos = cursor.fetchone()[0]
            
            if tratamientos_activos > 0:
                messagebox.showwarning(
                    "Paciente con Tratamientos Activos",
                    f"Este paciente tiene {tratamientos_activos} tratamiento(s) activo(s).\n\n"
                    "No se puede desvincular mientras tenga tratamientos activos."
                )
                return

            # Eliminar relación en tabla intermedia
            cursor.execute("""
                DELETE FROM Cuidador_Paciente 
                WHERE id_cuidador = ? AND id_paciente = ?
            """, (id_cuidador, paciente_id))

            # Verificar si el paciente tiene otros cuidadores
            cursor.execute("""
                SELECT COUNT(*) FROM Cuidador_Paciente 
                WHERE id_paciente = ?
            """, (paciente_id,))
            
            vinculaciones = cursor.fetchone()[0]

            # Si no tiene otros cuidadores, eliminar el paciente
            if vinculaciones == 0:
                cursor.execute("""
                    UPDATE Paciente SET activo = 0 
                    WHERE id_paciente = ?
                """, (paciente_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Paciente desvinculado correctamente.")
            cargar_datos()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el paciente:\n{str(e)}")

    # Barra de herramientas con botones
    toolbar_frame = ctk.CTkFrame(main_frame, height=40)
    toolbar_frame.pack(fill="x", pady=(5, 0))
    
    agregar_btn = ctk.CTkButton(toolbar_frame, text="Agregar Paciente", 
                               command=agregar_paciente, width=150)
    agregar_btn.pack(side="left", padx=5)
    
    eliminar_btn = ctk.CTkButton(toolbar_frame, text="Desvincular Paciente", 
                                command=eliminar_paciente, width=150,
                                fg_color="#d9534f", hover_color="#c9302c")
    eliminar_btn.pack(side="left", padx=5)
    
    refresh_btn = ctk.CTkButton(toolbar_frame, text="Actualizar Lista", 
                               command=cargar_datos, width=120)
    refresh_btn.pack(side="right", padx=5)

    # Barra de estado
    status_frame = ctk.CTkFrame(main_frame, height=25)
    status_frame.pack(fill="x", pady=(5, 0))
    
    status_label = ctk.CTkLabel(status_frame, text=f"Cuidador ID: {id_cuidador} | Total pacientes: 0")
    status_label.pack(side="left", padx=10)
    
    # Función para actualizar la barra de estado
    def actualizar_status():
        count = len(tree.get_children())
        status_label.configure(text=f"Cuidador ID: {id_cuidador} | Total pacientes: {count}")
    
    # Configurar evento para actualizar el estado
    tree.bind("<<TreeviewSelect>>", lambda e: actualizar_status())
    
    # Cargar datos iniciales
    cargar_datos()
    actualizar_status()