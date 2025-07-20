import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def mostrar_pacientes(frame_dinamico, id_cuidador):
    # Limpiar frame dinámico
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    lbl = tk.Label(frame_dinamico, text="Listado de Pacientes", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    lbl.pack(pady=(10, 20))

    # Crear tabla Treeview
    columnas = (
        "ID", "Nombre", "Edad", "Género",
        "Contacto Emergencia", "Activo",
        "Tratamientos Totales", "Tratamientos Activos"
    )

    tree = ttk.Treeview(frame_dinamico, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_FILENAME = os.path.join(BASE_DIR, "..", "..", "data", "MediCareDesk.db")

    def cargar_datos():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()
            # Filtrar por cuidador actual
            cursor.execute("""
                SELECT 
                    id_paciente, nombre, edad, genero,
                    contacto_emergencia, activo,
                    tratamientos_totales, tratamientos_activos
                FROM Vista_Pacientes
                WHERE id_cuidador = ?
            """, (id_cuidador,))
            filas = cursor.fetchall()
            for fila in filas:
                tree.insert("", "end", values=fila)
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al cargar datos: {e}")

    def agregar_paciente():
        form = tk.Toplevel()
        form.title("Agregar Paciente")
        form.geometry("400x400")

        tk.Label(form, text="Nombre:").pack()
        nombre_entry = tk.Entry(form)
        nombre_entry.pack()

        tk.Label(form, text="Edad:").pack()
        edad_entry = tk.Entry(form)
        edad_entry.pack()

        tk.Label(form, text="Género: (M/F/Otro)").pack()
        genero_entry = tk.Entry(form)
        genero_entry.pack()

        tk.Label(form, text="Contacto Emergencia:").pack()
        contacto_entry = tk.Entry(form)
        contacto_entry.pack()

        tk.Label(form, text="Observaciones:").pack()
        observaciones_entry = tk.Text(form)
        observaciones_entry.pack()

        def guardar_paciente():
            nombre = nombre_entry.get()
            edad = edad_entry.get()
            genero = genero_entry.get()
            contacto = contacto_entry.get()
            observaciones = observaciones_entry.get("1.0", tk.END).strip()

            if not nombre or not edad or not genero or not contacto:
                tk.messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                conn = sqlite3.connect(DB_FILENAME)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO Paciente (nombre, edad, genero, contacto_emergencia, observaciones)
                    VALUES (?, ?, ?, ?, ?)
                    """, (nombre, edad, genero, contacto, observaciones))

                id_paciente = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO Cuidador_Paciente (id_cuidador, id_paciente)
                    VALUES (?, ?)
                """, (id_cuidador, id_paciente))

                conn.commit()
                conn.close()

                tk.messagebox.showinfo("Éxito", "Paciente agregado y asignado correctamente.")
                form.destroy()
                cargar_datos()
            except sqlite3.Error as e:
                tk.messagebox.showerror("Error", f"Error al guardar el paciente: {e}")

        ctk.CTkButton(form, text="Guardar", command=guardar_paciente).pack(pady=10)

    def eliminar_paciente():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Seleccione un paciente para eliminar.")
            return

        paciente_id = tree.item(selected_item, "values")[0]
        try:
            conn = sqlite3.connect(DB_FILENAME)
            cursor = conn.cursor()

            # ⚠️ Eliminar relación en tabla intermedia:
            cursor.execute("""
                DELETE FROM Cuidador_Paciente WHERE id_cuidador = ? AND id_paciente = ?
            """, (id_cuidador, paciente_id))

            # Opcional: si quieres borrar COMPLETAMENTE el paciente (solo si no tiene otros cuidadores):
            cursor.execute("""
                SELECT COUNT(*) FROM Cuidador_Paciente WHERE id_paciente = ?
            """, (paciente_id,))
            vinculaciones = cursor.fetchone()[0]

            if vinculaciones == 0:
                cursor.execute("DELETE FROM Paciente WHERE id_paciente = ?", (paciente_id,))

            conn.commit()
            conn.close()

            tk.messagebox.showinfo("Éxito", "Paciente desvinculado correctamente.")
            cargar_datos()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"Error al eliminar el paciente: {e}")

    btn_frame = tk.Frame(frame_dinamico, bg="#f0f0f0")
    btn_frame.pack(pady=10)

    agregar_btn = ctk.CTkButton(btn_frame, text="Agregar Paciente", command=agregar_paciente)
    agregar_btn.pack(side=tk.LEFT, padx=10)

    eliminar_btn = ctk.CTkButton(btn_frame, text="Eliminar Paciente", command=eliminar_paciente)
    eliminar_btn.pack(side=tk.LEFT, padx=10)

    cargar_datos()
