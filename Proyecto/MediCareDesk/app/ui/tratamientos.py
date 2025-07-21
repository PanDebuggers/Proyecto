
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app.db import modelos

def mostrar_tratamientos(frame_dinamico):
    for widget in frame_dinamico.winfo_children():
        widget.destroy()

    # --- Frame principal ---
    main_frame = ctk.CTkFrame(frame_dinamico)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Filtros ---
    filtro_paciente = tk.StringVar()
    filtro_estado = tk.StringVar()
    filtro_tratamiento = tk.StringVar()

    filtro_frame = ctk.CTkFrame(main_frame)
    filtro_frame.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(filtro_frame, text="Filtrar por paciente:").pack(side="left", padx=5)
    pacientes = modelos.obtener_pacientes()
    pacientes_nombres = [f"{p['id_paciente']} - {p['nombre']}" for p in pacientes]
    # Crear un diccionario paciente_id -> cuidador (responsable)
    cuidadores_cache = {}
    for p in pacientes:
        id_cuidador = p.get('id_cuidador')
        if id_cuidador and id_cuidador not in cuidadores_cache:
            cuidador = modelos.buscar_cuidador_por_id(id_cuidador) if hasattr(modelos, 'buscar_cuidador_por_id') else None
            if cuidador:
                cuidadores_cache[id_cuidador] = cuidador['nombre']
    ctk.CTkOptionMenu(filtro_frame, values=["Todos"]+pacientes_nombres, variable=filtro_paciente).pack(side="left", padx=5)
    ctk.CTkLabel(filtro_frame, text="Estado:").pack(side="left", padx=5)
    estados = ['activo', 'suspendido', 'finalizado', 'pendiente']
    ctk.CTkOptionMenu(filtro_frame, values=["Todos"]+estados, variable=filtro_estado).pack(side="left", padx=5)
    ctk.CTkLabel(filtro_frame, text="Buscar tratamiento:").pack(side="left", padx=5)
    tk.Entry(filtro_frame, textvariable=filtro_tratamiento, width=20).pack(side="left", padx=5)

    # --- Tabla de tratamientos ---
    columnas = ("ID", "Paciente", "Edad", "Tratamiento", "Objetivo", "Fecha inicio", "Fecha fin", "Estado", "Responsable")
    tabla = ttk.Treeview(main_frame, columns=columnas, show="headings", height=18)  # Más filas visibles
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=110 if col!="Objetivo" else 180, anchor="center")
    tabla.pack(fill="x", pady=5)

    # --- Botones de acción ---
    btns_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btns_frame.pack(fill="x", pady=5)
    ctk.CTkButton(btns_frame, text="Agregar tratamiento", command=lambda: mostrar_formulario_tratamiento()).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Eliminar tratamiento", fg_color="#d9534f", hover_color="#c9302c", command=lambda: eliminar_tratamiento()).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Asignar medicamento", command=lambda: mostrar_formulario_medicamento()).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Actualizar", command=lambda: cargar_tabla()).pack(side="right", padx=5)

    # --- Cargar datos en tabla ---
    def cargar_tabla():
        tabla.delete(*tabla.get_children())
        paciente_filtro = filtro_paciente.get()
        estado_filtro = filtro_estado.get()
        texto_filtro = filtro_tratamiento.get().lower()
        tratamientos = modelos.obtener_tratamientos()
        for t in tratamientos:
            p = next((p for p in pacientes if p['id_paciente']==t['id_paciente']), None)
            if not p:
                continue
            nombre_paciente = f"{p['id_paciente']} - {p['nombre']}"
            if paciente_filtro and paciente_filtro != "Todos" and nombre_paciente != paciente_filtro:
                continue
            if estado_filtro and estado_filtro != "Todos" and t['estado'] != estado_filtro:
                continue
            if texto_filtro and texto_filtro not in t['nombre_tratamiento'].lower():
                continue
            # Buscar nombre del cuidador/responsable
            nombre_responsable = None
            id_cuidador = p.get('id_cuidador')
            if id_cuidador:
                if id_cuidador in cuidadores_cache:
                    nombre_responsable = cuidadores_cache[id_cuidador]
                else:
                    # Fallback: buscar por función si no está en cache
                    cuidador = modelos.buscar_cuidador_por_id(id_cuidador) if hasattr(modelos, 'buscar_cuidador_por_id') else None
                    if cuidador:
                        nombre_responsable = cuidador['nombre']
                        cuidadores_cache[id_cuidador] = nombre_responsable
            tabla.insert("", "end", values=(t['id_tratamiento'], nombre_paciente, p['edad'], t['nombre_tratamiento'], t.get('descripcion',''), t['fecha_inicio'], t['fecha_fin'], t['estado'], nombre_responsable or ""))

    filtro_paciente.trace_add('write', lambda *a: cargar_tabla())
    filtro_estado.trace_add('write', lambda *a: cargar_tabla())
    filtro_tratamiento.trace_add('write', lambda *a: cargar_tabla())
    cargar_tabla()

    # --- Formulario para agregar tratamiento ---
    def mostrar_formulario_tratamiento():
        win = ctk.CTkToplevel(main_frame)
        win.title("Agregar tratamiento")
        win.geometry("500x500")
        win.grab_set()
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        paciente_var = tk.StringVar(value=pacientes_nombres[0] if pacientes_nombres else "")
        edad_var = tk.StringVar()
        tratamiento_var = tk.StringVar()
        objetivo_var = tk.StringVar()
        fecha_inicio_var = tk.StringVar()
        fecha_fin_var = tk.StringVar()
        estado_var = tk.StringVar(value=estados[0])
        responsable_var = tk.StringVar()

        row=0
        ctk.CTkLabel(frame, text="Paciente:").grid(row=row, column=0, sticky="w", pady=5)
        paciente_menu = ctk.CTkOptionMenu(frame, values=pacientes_nombres, variable=paciente_var)
        paciente_menu.grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Edad:").grid(row=row, column=0, sticky="w", pady=5)
        edad_entry = ctk.CTkEntry(frame, textvariable=edad_var)
        edad_entry.grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Tratamiento:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkEntry(frame, textvariable=tratamiento_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Objetivo:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkEntry(frame, textvariable=objetivo_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Fecha inicio:").grid(row=row, column=0, sticky="w", pady=5)
        DateEntry(frame, textvariable=fecha_inicio_var, date_pattern='yyyy-mm-dd').grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Fecha fin:").grid(row=row, column=0, sticky="w", pady=5)
        DateEntry(frame, textvariable=fecha_fin_var, date_pattern='yyyy-mm-dd').grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Estado:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=estados, variable=estado_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Responsable:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkEntry(frame, textvariable=responsable_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1

        def guardar():
            try:
                paciente_sel = paciente_var.get()
                id_paciente = int(paciente_sel.split(' - ')[0])
                datos = {
                    'id_paciente': id_paciente,
                    'nombre_tratamiento': tratamiento_var.get(),
                    'descripcion': objetivo_var.get(),
                    'estado': estado_var.get(),
                    'fecha_inicio': fecha_inicio_var.get(),
                    'fecha_fin': fecha_fin_var.get()
                }
                modelos.crear_tratamiento(datos)
                messagebox.showinfo("Éxito", "Tratamiento agregado correctamente.")
                win.grab_release()
                win.destroy()
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame, text="Guardar", command=guardar).grid(row=row, column=1, sticky="e", pady=10)

    # --- Eliminar tratamiento ---
    def eliminar_tratamiento():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un tratamiento para eliminar.")
            return
        item = tabla.item(sel[0])
        id_tratamiento = item['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar el tratamiento seleccionado?"):
            conn = modelos.obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tratamiento WHERE id_tratamiento = ?", (id_tratamiento,))
            conn.commit()
            conn.close()
            cargar_tabla()

    # --- Formulario para asignar medicamento ---
    def mostrar_formulario_medicamento():
        sel = tabla.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un tratamiento para asignar medicamento.")
            return
        item = tabla.item(sel[0])
        id_tratamiento = item['values'][0]
        win = ctk.CTkToplevel(main_frame)
        win.title("Asignar medicamento")
        win.geometry("500x350")
        win.transient(main_frame.winfo_toplevel())
        win.grab_set()
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        medicamentos = modelos.obtener_medicamentos()
        medicamentos_nombres = [m['nombre'] for m in medicamentos]
        medicamentos_dict = {m['nombre']: m['id_medicamento'] for m in medicamentos}
        frecuencia_opciones = ['una_vez_al_dia','cada_8_horas','cada_12_horas','cada_24_horas','personalizada']
        via_opciones = ['oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea','inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica']
        estado_opciones = ['activo', 'suspendido', 'finalizado', 'pendiente']

        medicamento_var = tk.StringVar()
        dosis_var = tk.StringVar()
        frecuencia_var = tk.StringVar(value=frecuencia_opciones[0])
        via_var = tk.StringVar(value=via_opciones[0])
        hora_var = tk.StringVar()
        estado_var = tk.StringVar(value=estado_opciones[0])

        row=0
        ctk.CTkLabel(frame, text="Medicamento:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=medicamentos_nombres, variable=medicamento_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Dosis:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkEntry(frame, textvariable=dosis_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Frecuencia:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=frecuencia_opciones, variable=frecuencia_var).grid(row=row, column=1, sticky="ew", pady=5)
        row=0
        ctk.CTkLabel(frame, text="Medicamento:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=medicamentos_nombres, variable=medicamento_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Dosis:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkEntry(frame, textvariable=dosis_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Frecuencia:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=frecuencia_opciones, variable=frecuencia_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Vía de administración:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=via_opciones, variable=via_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1
        ctk.CTkLabel(frame, text="Estado:").grid(row=row, column=0, sticky="w", pady=5)
        ctk.CTkOptionMenu(frame, values=estado_opciones, variable=estado_var).grid(row=row, column=1, sticky="ew", pady=5)
        row+=1


        def guardar():
            try:
                nombre_medicamento = medicamento_var.get()
                id_medicamento = medicamentos_dict.get(nombre_medicamento)
                # Obtener fechas del tratamiento asociado
                tratamiento = modelos.obtener_tratamiento(id_tratamiento)
                fecha_inicio = tratamiento['fecha_inicio']
                fecha_fin = tratamiento['fecha_fin']
                datos = {
                    'id_tratamiento': id_tratamiento,
                    'id_medicamento': id_medicamento,
                    'dosis': dosis_var.get(),
                    'frecuencia': frecuencia_var.get(),
                    'via_administracion': via_var.get(),
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'estado': estado_var.get()
                }
                from app.logic import tratamientos as logic_tratamientos
                asignacion_id = logic_tratamientos.asignar_medicamento_a_tratamiento(**datos)
                logic_tratamientos.generar_tomas_tratamiento(asignacion_id)
                messagebox.showinfo("Éxito", "Medicamento asignado y tomas generadas correctamente.")
                win.grab_release()
                win.destroy()
            except Exception as e:
                try:
                    win.grab_release()
                except:
                    pass
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame, text="Guardar", command=guardar).grid(row=row, column=1, sticky="e", pady=10)
        ctk.CTkButton(frame, text="Cancelar", command=lambda: (win.grab_release(), win.destroy()), fg_color="gray").grid(row=row, column=0, sticky="w", pady=10)