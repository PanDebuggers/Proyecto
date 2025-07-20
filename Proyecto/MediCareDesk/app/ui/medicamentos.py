import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def mostrar_medicamentos(frame_dinamico):
    # Limpiar frame dinámico
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    # Frame principal con scroll
    main_frame = tk.Frame(frame_dinamico, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Canvas y scrollbar
    canvas = tk.Canvas(main_frame, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Título
    lbl = tk.Label(scrollable_frame, text="Gestión de Medicamentos", 
                  font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    lbl.pack(pady=(10, 20))

    # Crear tabla Treeview con estilo mejorado
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    columnas = (
        "ID", "Nombre", "Principio Activo", "Presentación",
        "Laboratorio", "Caducidad", "Registro"
    )

    tree = ttk.Treeview(scrollable_frame, columns=columnas, show="headings", selectmode="browse")
    
    # Configurar columnas
    tree.column("ID", width=50, anchor="center")
    tree.column("Nombre", width=150, anchor="w")
    tree.column("Principio Activo", width=150, anchor="w")
    tree.column("Presentación", width=120, anchor="center")
    tree.column("Laboratorio", width=120, anchor="w")
    tree.column("Caducidad", width=100, anchor="center")
    tree.column("Registro", width=120, anchor="center")

    for col in columnas:
        tree.heading(col, text=col)

    tree.pack(fill="both", expand=True, padx=5, pady=5)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_FILENAME = os.path.join(BASE_DIR, "..", "..", "data", "MediCareDesk.db")
    
    # Función para cargar datos
    def cargar_datos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    id_medicamento, nombre, principio_activo,
                    presentacion, laboratorio,
                    fecha_caducidad, fecha_registro
                FROM Medicamento
                ORDER BY nombre
            """)
            
            filas = cursor.fetchall()
            
            # Insertar datos con etiquetas alternas
            for i, fila in enumerate(filas):
                # Formatear fecha de caducidad
                if fila[5]:  # fecha_caducidad
                    fecha_cad = fila[5].split()[0]  # Solo fecha sin hora
                else:
                    fecha_cad = "N/A"
                
                # Formatear fecha de registro
                fecha_reg = fila[6].split()[0] if fila[6] else "N/A"
                
                # Crear nueva tupla con fechas formateadas
                fila_formateada = fila[:5] + (fecha_cad, fecha_reg)
                
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                tree.insert("", "end", values=fila_formateada, tags=tags)
                
            conn.close()
            
            # Configurar colores alternos
            tree.tag_configure('evenrow', background='#ffffff')
            tree.tag_configure('oddrow', background='#f5f5f5')
            
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error de Base de Datos", 
                                  f"No se pudieron cargar los medicamentos:\n{str(e)}")

    # Función para agregar medicamento
    def agregar_medicamento():
        form = tk.Toplevel()
        form.title("Agregar Nuevo Medicamento")
        form.geometry("500x600")

        # Campos del formulario
        campos = [
            ("Nombre:", ""),
            ("Principio Activo:", ""),
            ("Presentación:", "Comprimidas"),
            ("Laboratorio:", ""),
            ("Fecha Caducidad (YYYY-MM-DD):", ""),
            ("Indicaciones:", ""),
            ("Contraindicaciones:", "")
        ]

        entries = []
        for i, (label, default) in enumerate(campos[:5]):  # Los primeros 5 son Entry
            tk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="we")
            entry.insert(0, default)
            entries.append(entry)

        # Menú desplegable para presentación
        presentaciones = ['Comprimidas', 'Jarabe', 'Crema', 'Solución inyectable', 'otros']
        entries[2].destroy()  # Eliminar el Entry existente
        presentacion_var = tk.StringVar(value=presentaciones[0])
        tk.Label(form, text="Presentación:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        presentacion_menu = ttk.Combobox(form, textvariable=presentacion_var, values=presentaciones, state="readonly")
        presentacion_menu.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        entries[2] = presentacion_var

        # Áreas de texto para indicaciones y contraindicaciones
        tk.Label(form, text=campos[5][0]).grid(row=5, column=0, padx=10, pady=5, sticky="ne")
        indicaciones_entry = tk.Text(form, height=5, width=30)
        indicaciones_entry.grid(row=5, column=1, padx=10, pady=5, sticky="we")

        tk.Label(form, text=campos[6][0]).grid(row=6, column=0, padx=10, pady=5, sticky="ne")
        contraindicaciones_entry = tk.Text(form, height=5, width=30)
        contraindicaciones_entry.grid(row=6, column=1, padx=10, pady=5, sticky="we")

        def guardar_medicamento():
            # Obtener valores de los campos
            nombre = entries[0].get()
            principio_activo = entries[1].get()
            presentacion = entries[2].get()
            laboratorio = entries[3].get()
            fecha_caducidad = entries[4].get()
            indicaciones = indicaciones_entry.get("1.0", tk.END).strip()
            contraindicaciones = contraindicaciones_entry.get("1.0", tk.END).strip()

            # Validaciones básicas
            if not nombre:
                tk.messagebox.showerror("Error", "El nombre del medicamento es obligatorio")
                return

            try:
                conn = sqlite3.connect(DB_FILENAME)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO Medicamento (
                        nombre, principio_activo, presentacion,
                        laboratorio, fecha_caducidad,
                        indicaciones, contraindicaciones
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    nombre, principio_activo, presentacion,
                    laboratorio, fecha_caducidad,
                    indicaciones, contraindicaciones
                ))
                
                conn.commit()
                conn.close()
                
                tk.messagebox.showinfo("Éxito", "Medicamento agregado correctamente")
                form.destroy()
                cargar_datos()
                
            except sqlite3.Error as e:
                tk.messagebox.showerror("Error", f"No se pudo agregar el medicamento:\n{str(e)}")

        btn_guardar = ctk.CTkButton(form, text="Guardar Medicamento", command=guardar_medicamento)
        btn_guardar.grid(row=7, column=1, pady=10, sticky="e")

    # Función para editar medicamento
    def editar_medicamento():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Selección requerida", "Por favor seleccione un medicamento para editar.")
            return

        medicamento_data = tree.item(selected_item, "values")
        medicamento_id = medicamento_data[0]

        # Obtener datos completos de la base de datos
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Medicamento WHERE id_medicamento = ?", (medicamento_id,))
            medicamento = cursor.fetchone()
            conn.close()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"No se pudo obtener los datos del medicamento:\n{str(e)}")
            return

        form = tk.Toplevel()
        form.title(f"Editar Medicamento ID: {medicamento_id}")
        form.geometry("500x600")

        # Campos del formulario con datos actuales
        campos = [
            ("Nombre:", medicamento[1]),  # nombre
            ("Principio Activo:", medicamento[2]),  # principio_activo
            ("Presentación:", medicamento[6]),  # presentacion
            ("Laboratorio:", medicamento[7]),  # laboratorio
            ("Fecha Caducidad (YYYY-MM-DD):", medicamento[4] or ""),  # fecha_caducidad
            ("Indicaciones:", medicamento[3] or ""),  # indicaciones
            ("Contraindicaciones:", medicamento[5] or "")  # contraindicaciones
        ]

        entries = []
        for i, (label, default) in enumerate(campos[:5]):  # Los primeros 5 son Entry
            tk.Label(form, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(form)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="we")
            entry.insert(0, default)
            entries.append(entry)

        # Menú desplegable para presentación
        presentaciones = ['Comprimidas', 'Jarabe', 'Crema', 'Solución inyectable', 'otros']
        entries[2].destroy()  # Eliminar el Entry existente
        presentacion_var = tk.StringVar(value=medicamento[6])
        tk.Label(form, text="Presentación:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        presentacion_menu = ttk.Combobox(form, textvariable=presentacion_var, values=presentaciones, state="readonly")
        presentacion_menu.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        entries[2] = presentacion_var

        # Áreas de texto para indicaciones y contraindicaciones
        tk.Label(form, text=campos[5][0]).grid(row=5, column=0, padx=10, pady=5, sticky="ne")
        indicaciones_entry = tk.Text(form, height=5, width=30)
        indicaciones_entry.grid(row=5, column=1, padx=10, pady=5, sticky="we")
        indicaciones_entry.insert("1.0", campos[5][1])

        tk.Label(form, text=campos[6][0]).grid(row=6, column=0, padx=10, pady=5, sticky="ne")
        contraindicaciones_entry = tk.Text(form, height=5, width=30)
        contraindicaciones_entry.grid(row=6, column=1, padx=10, pady=5, sticky="we")
        contraindicaciones_entry.insert("1.0", campos[6][1])

        def actualizar_medicamento():
            # Obtener valores de los campos
            nombre = entries[0].get()
            principio_activo = entries[1].get()
            presentacion = entries[2].get()
            laboratorio = entries[3].get()
            fecha_caducidad = entries[4].get()
            indicaciones = indicaciones_entry.get("1.0", tk.END).strip()
            contraindicaciones = contraindicaciones_entry.get("1.0", tk.END).strip()

            # Validaciones básicas
            if not nombre:
                tk.messagebox.showerror("Error", "El nombre del medicamento es obligatorio")
                return

            try:
                conn = sqlite3.connect(DB_FILENAME)
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE Medicamento SET
                        nombre = ?,
                        principio_activo = ?,
                        presentacion = ?,
                        laboratorio = ?,
                        fecha_caducidad = ?,
                        indicaciones = ?,
                        contraindicaciones = ?
                    WHERE id_medicamento = ?
                """, (
                    nombre, principio_activo, presentacion,
                    laboratorio, fecha_caducidad,
                    indicaciones, contraindicaciones,
                    medicamento_id
                ))
                
                conn.commit()
                conn.close()
                
                tk.messagebox.showinfo("Éxito", "Medicamento actualizado correctamente")
                form.destroy()
                cargar_datos()
                
            except sqlite3.Error as e:
                tk.messagebox.showerror("Error", f"No se pudo actualizar el medicamento:\n{str(e)}")

        btn_guardar = ctk.CTkButton(form, text="Guardar Cambios", command=actualizar_medicamento)
        btn_guardar.grid(row=7, column=1, pady=10, sticky="e")

    # Función para eliminar medicamento
    def eliminar_medicamento():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Selección requerida", "Por favor seleccione un medicamento para eliminar.")
            return

        medicamento_id = tree.item(selected_item, "values")[0]
        medicamento_nombre = tree.item(selected_item, "values")[1]

        # Confirmación antes de eliminar
        confirmar = tk.messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el medicamento '{medicamento_nombre}' (ID: {medicamento_id})?\n\n"
            "Nota: Esta acción no se puede deshacer."
        )
        
        if not confirmar:
            return

        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            
            # Verificar si el medicamento está en uso
            cursor.execute("""
                SELECT COUNT(*) FROM Tratamiento_Medicamento 
                WHERE id_medicamento = ?
            """, (medicamento_id,))
            
            en_uso = cursor.fetchone()[0]
            
            if en_uso > 0:
                tk.messagebox.showwarning(
                    "Medicamento en Uso",
                    f"Este medicamento está asignado a {en_uso} tratamiento(s).\n\n"
                    "No se puede eliminar mientras esté en uso."
                )
                return
            
            # Eliminar el medicamento
            cursor.execute("DELETE FROM Medicamento WHERE id_medicamento = ?", (medicamento_id,))
            
            conn.commit()
            conn.close()
            
            tk.messagebox.showinfo("Éxito", "Medicamento eliminado correctamente")
            cargar_datos()
            
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"No se pudo eliminar el medicamento:\n{str(e)}")

    # Botones de acción
    btn_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
    btn_frame.pack(pady=10)

    btn_agregar = ctk.CTkButton(btn_frame, text="Agregar Medicamento", command=agregar_medicamento)
    btn_agregar.pack(side=tk.LEFT, padx=5)

    btn_editar = ctk.CTkButton(btn_frame, text="Editar Medicamento", command=editar_medicamento)
    btn_editar.pack(side=tk.LEFT, padx=5)

    btn_eliminar = ctk.CTkButton(btn_frame, text="Eliminar Medicamento", command=eliminar_medicamento,
                                fg_color="#d9534f", hover_color="#c9302c")
    btn_eliminar.pack(side=tk.LEFT, padx=5)

    btn_refresh = ctk.CTkButton(btn_frame, text="Refrescar", command=cargar_datos)
    btn_refresh.pack(side=tk.LEFT, padx=5)

    # Cargar datos iniciales
    cargar_datos()