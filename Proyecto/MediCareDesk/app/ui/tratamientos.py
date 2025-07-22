import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app.db import modelos

# Lista global para rastrear diálogos abiertos
open_dialogs = []

def limpiar_ventanas_modales(root):
    """Función para limpiar todas las ventanas modales de manera segura"""
    try:
        # Limpiar ventanas Toplevel estándar
        for widget in list(root.winfo_children()):
            if isinstance(widget, tk.Toplevel):
                try:
                    widget.grab_release()
                    widget.destroy()
                except:
                    pass
        
        # Limpiar ventanas CTkToplevel
        for widget in list(root.winfo_children()):
            if hasattr(widget, '__class__') and 'CTkToplevel' in str(widget.__class__):
                try:
                    widget.grab_release()
                    widget.destroy()
                except:
                    pass
    except:
        pass

def mostrar_tratamientos(frame_dinamico):
    # Obtener ventana principal
    try:
        root = frame_dinamico.winfo_toplevel()
        
        # Limpiar ventanas modales existentes
        limpiar_ventanas_modales(root)
        
        # Limpiar lista global
        global open_dialogs
        for dialog in open_dialogs[:]:
            try:
                if hasattr(dialog, 'winfo_exists') and dialog.winfo_exists():
                    dialog.grab_release()
                    dialog.destroy()
            except:
                pass
        open_dialogs.clear()
        
        # Asegurar que la ventana principal tenga el foco
        root.focus_force()
        root.lift()
        
    except Exception as e:
        print(f"Error en limpieza inicial: {e}")
    
    # Limpiar contenido del frame
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
    
    try:
        pacientes = modelos.obtener_pacientes()
        pacientes_nombres = [f"{p['id_paciente']} - {p['nombre']}" for p in pacientes]
    except:
        pacientes = []
        pacientes_nombres = []
    
    ctk.CTkOptionMenu(filtro_frame, values=["Todos"]+pacientes_nombres, variable=filtro_paciente).pack(side="left", padx=5)
    ctk.CTkLabel(filtro_frame, text="Estado:").pack(side="left", padx=5)
    estados = ['activo', 'suspendido', 'finalizado', 'pendiente']
    ctk.CTkOptionMenu(filtro_frame, values=["Todos"]+estados, variable=filtro_estado).pack(side="left", padx=5)
    ctk.CTkLabel(filtro_frame, text="Buscar tratamiento:").pack(side="left", padx=5)
    tk.Entry(filtro_frame, textvariable=filtro_tratamiento, width=20).pack(side="left", padx=5)

    # --- Tabla de tratamientos ---
    columnas = ("ID", "Paciente", "Edad", "Tratamiento", "Objetivo", "Fecha inicio", "Fecha fin", "Estado", "Responsable")
    tabla = ttk.Treeview(main_frame, columns=columnas, show="headings", height=18)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=110 if col!="Objetivo" else 180, anchor="center")
    tabla.pack(fill="x", pady=5)

    # --- Botones de acción ---
    btns_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btns_frame.pack(fill="x", pady=5)
    ctk.CTkButton(btns_frame, text="Agregar tratamiento", command=lambda: mostrar_formulario_tratamiento(main_frame, tabla, pacientes_nombres, estados, cargar_tabla)).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Eliminar tratamiento", fg_color="#d9534f", hover_color="#c9302c", command=lambda: eliminar_tratamiento(tabla, cargar_tabla)).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Asignar medicamento", command=lambda: mostrar_formulario_medicamento(main_frame, tabla, cargar_tabla)).pack(side="left", padx=5)
    ctk.CTkButton(btns_frame, text="Actualizar", command=lambda: cargar_tabla()).pack(side="right", padx=5)

    # --- Cargar datos en tabla ---
    def cargar_tabla():
        tabla.delete(*tabla.get_children())
        try:
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
                tabla.insert("", "end", values=(t['id_tratamiento'], nombre_paciente, p['edad'], t['nombre_tratamiento'], t.get('descripcion',''), t['fecha_inicio'], t['fecha_fin'], t['estado'], p.get('contacto','')))
        except Exception as e:
            print(f"Error cargando tabla: {e}")

    filtro_paciente.trace_add('write', lambda *a: cargar_tabla())
    filtro_estado.trace_add('write', lambda *a: cargar_tabla())
    filtro_tratamiento.trace_add('write', lambda *a: cargar_tabla())
    cargar_tabla()

def cerrar_ventana_simple(window):
    """Función simple para cerrar ventanas sin grab_set"""
    global open_dialogs
    try:
        if window in open_dialogs:
            open_dialogs.remove(window)
        window.destroy()
    except:
        pass

def mostrar_formulario_tratamiento(parent_frame, tabla, pacientes_nombres, estados, cargar_tabla_callback):
    global open_dialogs
    
    # Crear ventana SIN grab_set para evitar el difuminado
    win = tk.Toplevel(parent_frame.winfo_toplevel())
    win.title("Agregar tratamiento")
    win.geometry("500x600")
    win.overrideredirect(False)
    win.attributes('-topmost', True)
    win.transient(parent_frame.winfo_toplevel())
    win.lift()
    win.focus_set()
    
    # Agregar a la lista
    open_dialogs.append(win)
    
    # NO usar grab_set - esto evita el difuminado
    win.transient(parent_frame.winfo_toplevel())
    win.lift()
    win.focus_set()
    
    # Protocolo de cierre simple
    win.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_simple(win))
    
    frame = ctk.CTkScrollableFrame(win)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Variables del formulario
    paciente_var = tk.StringVar(value=pacientes_nombres[0] if pacientes_nombres else "")
    edad_var = tk.StringVar()
    tratamiento_var = tk.StringVar()
    objetivo_var = tk.StringVar()
    fecha_inicio_var = tk.StringVar()
    fecha_fin_var = tk.StringVar()
    estado_var = tk.StringVar(value=estados[0] if estados else "activo")
    responsable_var = tk.StringVar()

    row = 0
    # Paciente
    ctk.CTkLabel(frame, text="Paciente:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    if pacientes_nombres:
        ctk.CTkOptionMenu(frame, values=pacientes_nombres, variable=paciente_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    else:
        ctk.CTkLabel(frame, text="No hay pacientes", fg_color="red").grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Tratamiento
    ctk.CTkLabel(frame, text="Tratamiento:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkEntry(frame, textvariable=tratamiento_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Objetivo
    ctk.CTkLabel(frame, text="Objetivo:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    objetivo_entry = ctk.CTkTextbox(frame, height=80)
    objetivo_entry.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Fecha inicio
    ctk.CTkLabel(frame, text="Fecha inicio (YYYY-MM-DD):").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkEntry(frame, textvariable=fecha_inicio_var, placeholder_text="2024-01-15").grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Fecha fin
    ctk.CTkLabel(frame, text="Fecha fin (YYYY-MM-DD):").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkEntry(frame, textvariable=fecha_fin_var, placeholder_text="2024-02-15").grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Estado
    ctk.CTkLabel(frame, text="Estado:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkOptionMenu(frame, values=estados, variable=estado_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1

    # Configurar el grid
    frame.grid_columnconfigure(1, weight=1)

    def guardar():
        try:
            paciente_sel = paciente_var.get()
            if not paciente_sel or paciente_sel == "No hay pacientes":
                messagebox.showwarning("Error", "Selecciona un paciente")
                return
                
            if not tratamiento_var.get().strip():
                messagebox.showwarning("Error", "Ingresa el nombre del tratamiento")
                return
                
            id_paciente = int(paciente_sel.split(' - ')[0])
            objetivo_texto = objetivo_entry.get("1.0", "end-1c")
            
            datos = {
                'id_paciente': id_paciente,
                'nombre_tratamiento': tratamiento_var.get().strip(),
                'descripcion': objetivo_texto,
                'estado': estado_var.get(),
                'fecha_inicio': fecha_inicio_var.get() or None,
                'fecha_fin': fecha_fin_var.get() or None
            }
            
            modelos.crear_tratamiento(datos)
            messagebox.showinfo("Éxito", "Tratamiento agregado correctamente.")
            cerrar_ventana_simple(win)
            cargar_tabla_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    # Botones
    btn_frame = ctk.CTkFrame(frame)
    btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=20, padx=5)
    btn_frame.grid_columnconfigure(0, weight=1)
    btn_frame.grid_columnconfigure(1, weight=1)
    
    ctk.CTkButton(btn_frame, text="Cancelar", command=lambda: cerrar_ventana_simple(win), 
                  fg_color="gray", hover_color="#666666").grid(row=0, column=0, sticky="ew", padx=(0, 5))
    ctk.CTkButton(btn_frame, text="Guardar", command=guardar).grid(row=0, column=1, sticky="ew", padx=(5, 0))

def eliminar_tratamiento(tabla, cargar_tabla_callback):
    sel = tabla.selection()
    if not sel:
        messagebox.showwarning("Selecciona", "Selecciona un tratamiento para eliminar.")
        return
    item = tabla.item(sel[0])
    id_tratamiento = item['values'][0]
    if messagebox.askyesno("Confirmar", "¿Eliminar el tratamiento seleccionado?"):
        try:
            conn = modelos.obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tratamiento WHERE id_tratamiento = ?", (id_tratamiento,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Tratamiento eliminado correctamente.")
            cargar_tabla_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

def mostrar_formulario_medicamento(parent_frame, tabla, cargar_tabla_callback):
    global open_dialogs
    
    sel = tabla.selection()
    if not sel:
        messagebox.showwarning("Selecciona", "Selecciona un tratamiento para asignar medicamento.")
        return
    
    item = tabla.item(sel[0])
    id_tratamiento = item['values'][0]
    
    # Crear ventana SIN grab_set para evitar difuminado
    win = tk.Toplevel(parent_frame.winfo_toplevel())
    win.title("Asignar medicamento")
    win.geometry("500x500")

    win.overrideredirect(False)
    win.attributes('-topmost', True)
    win.transient(parent_frame.winfo_toplevel())
    win.lift()
    win.focus_set()
    
    open_dialogs.append(win)
    
    # NO usar grab_set
    win.transient(parent_frame.winfo_toplevel())
    win.lift()
    win.focus_set()
    
    win.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana_simple(win))
    
    frame = ctk.CTkScrollableFrame(win)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Obtener datos
    try:
        medicamentos = modelos.obtener_medicamentos()
        medicamentos_nombres = [m['nombre'] for m in medicamentos]
        medicamentos_dict = {m['nombre']: m['id_medicamento'] for m in medicamentos}
    except:
        medicamentos_nombres = []
        medicamentos_dict = {}
    
    frecuencia_opciones = ['una_vez_al_dia','cada_8_horas','cada_12_horas','cada_24_horas','personalizada']
    via_opciones = ['oral', 'intravenosa', 'topica', 'intramuscular', 'subcutanea','inhalatoria', 'rectal', 'sublingual', 'oftalmologica', 'otica', 'nasal', 'transdermica']
    estado_opciones = ['activo', 'suspendido', 'finalizado', 'pendiente']

    # Variables del formulario
    medicamento_var = tk.StringVar()
    dosis_var = tk.StringVar()
    frecuencia_var = tk.StringVar(value=frecuencia_opciones[0])
    via_var = tk.StringVar(value=via_opciones[0])
    estado_var = tk.StringVar(value=estado_opciones[0])

    row = 0
    # Medicamento
    ctk.CTkLabel(frame, text="Medicamento:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    if medicamentos_nombres:
        medicamento_var.set(medicamentos_nombres[0])
        ctk.CTkOptionMenu(frame, values=medicamentos_nombres, variable=medicamento_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    else:
        ctk.CTkLabel(frame, text="No hay medicamentos", fg_color="red").grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Dosis
    ctk.CTkLabel(frame, text="Dosis:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkEntry(frame, textvariable=dosis_var, placeholder_text="ej: 500mg").grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Frecuencia
    ctk.CTkLabel(frame, text="Frecuencia:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkOptionMenu(frame, values=frecuencia_opciones, variable=frecuencia_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Vía de administración
    ctk.CTkLabel(frame, text="Vía administración:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkOptionMenu(frame, values=via_opciones, variable=via_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1
    
    # Estado
    ctk.CTkLabel(frame, text="Estado:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
    ctk.CTkOptionMenu(frame, values=estado_opciones, variable=estado_var).grid(row=row, column=1, sticky="ew", pady=5, padx=5)
    row += 1

    frame.grid_columnconfigure(1, weight=1)

    def guardar():
        try:
            if not medicamentos_nombres:
                messagebox.showerror("Error", "No hay medicamentos disponibles")
                return
                
            nombre_medicamento = medicamento_var.get()
            if not nombre_medicamento:
                messagebox.showwarning("Error", "Selecciona un medicamento")
                return
                
            if not dosis_var.get().strip():
                messagebox.showwarning("Error", "Ingresa la dosis")
                return
                
            id_medicamento = medicamentos_dict.get(nombre_medicamento)
            if not id_medicamento:
                messagebox.showerror("Error", "Medicamento no válido")
                return
                
            datos = {
                'id_tratamiento': id_tratamiento,
                'id_medicamento': id_medicamento,
                'dosis': dosis_var.get().strip(),
                'frecuencia': frecuencia_var.get(),
                'via_administracion': via_var.get(),
                'fecha_inicio': None,
                'fecha_fin': None,
                'estado': estado_var.get()
            }
            
            from app.logic import tratamientos as logic_tratamientos
            asignacion_id = logic_tratamientos.asignar_medicamento_a_tratamiento(**datos)
            logic_tratamientos.generar_tomas_tratamiento(asignacion_id)
            messagebox.showinfo("Éxito", "Medicamento asignado y tomas generadas correctamente.")
            cerrar_ventana_simple(win)
        except Exception as e:
            messagebox.showerror("Error", f"Error al asignar medicamento: {str(e)}")

    # Botones
    btn_frame = ctk.CTkFrame(frame)
    btn_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=20, padx=5)
    btn_frame.grid_columnconfigure(0, weight=1)
    btn_frame.grid_columnconfigure(1, weight=1)
    
    ctk.CTkButton(btn_frame, text="Cancelar", command=lambda: cerrar_ventana_simple(win), 
                  fg_color="gray", hover_color="#666666").grid(row=0, column=0, sticky="ew", padx=(0, 5))
    ctk.CTkButton(btn_frame, text="Guardar", command=guardar).grid(row=0, column=1, sticky="ew", padx=(5, 0))