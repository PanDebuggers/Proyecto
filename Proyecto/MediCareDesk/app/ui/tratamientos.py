import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.db import modelos
from app.ui.base_view import BaseView

class TratamientosView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Tratamientos")
        
        self.pacientes = self._cargar_pacientes()
        self.medicamentos = self._cargar_medicamentos()
        
        self._crear_widgets()
        self._cargar_tabla()
    
    def _cargar_pacientes(self):
        """Carga la lista de pacientes activos desde la base de datos"""
        return modelos.obtener_pacientes(activos=True)
    
    def _cargar_medicamentos(self):
        """Carga la lista de medicamentos desde la base de datos"""
        return modelos.obtener_medicamentos()
    
    def _crear_widgets(self):
        """Crea los elementos de la interfaz"""

        self.frame_controles = ttk.Frame(self)
        self.frame_controles.pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Label(self.frame_controles, text="Paciente:").grid(row=0, column=0, padx=5)
        self.cb_paciente = ttk.Combobox(self.frame_controles, values=[f"{p['id_paciente']} - {p['nombre']}" for p in self.pacientes])
        self.cb_paciente.grid(row=0, column=1, padx=5, sticky=tk.EW)
        
        btn_filtrar = ttk.Button(self.frame_controles, text="Filtrar", command=self._filtrar_tratamientos)
        btn_filtrar.grid(row=0, column=2, padx=5)
        
        btn_agregar = ttk.Button(self.frame_controles, text="Agregar Tratamiento", command=self._abrir_formulario_tratamiento)
        btn_agregar.grid(row=0, column=3, padx=5)
        
        self.frame_tabla = ttk.Frame(self)
        self.frame_tabla.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        columns = ('id', 'paciente', 'nombre', 'estado', 'fecha_inicio', 'fecha_fin')
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columns, show='headings')
        
        self.tabla.heading('id', text='ID')
        self.tabla.heading('paciente', text='Paciente')
        self.tabla.heading('nombre', text='Nombre Tratamiento')
        self.tabla.heading('estado', text='Estado')
        self.tabla.heading('fecha_inicio', text='Fecha Inicio')
        self.tabla.heading('fecha_fin', text='Fecha Fin')
        
        self.tabla.column('id', width=50)
        self.tabla.column('paciente', width=150)
        self.tabla.column('nombre', width=150)
        self.tabla.column('estado', width=100)
        self.tabla.column('fecha_inicio', width=100)
        self.tabla.column('fecha_fin', width=100)
        
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.btn_asignar = ttk.Button(self.frame_controles, text="Asignar Medicamento", 
                                     command=self._abrir_asignar_medicamento, state=tk.DISABLED)
        self.btn_asignar.grid(row=0, column=4, padx=5)
        
        self.tabla.bind('<<TreeviewSelect>>', self._habilitar_boton_asignar)
    
    def _cargar_tabla(self, paciente_id=None):
        """Carga los tratamientos en la tabla, opcionalmente filtrados por paciente"""
        self.tabla.delete(*self.tabla.get_children())
        tratamientos = modelos.obtener_tratamientos(paciente_id)
        
        for t in tratamientos:
            paciente_nombre = next((f"{p['id_paciente']} - {p['nombre']}" for p in self.pacientes if p['id_paciente'] == t['id_paciente']), '')
            self.tabla.insert('', tk.END, values=(
                t['id_tratamiento'],
                paciente_nombre,
                t['nombre_tratamiento'],
                t['estado'].capitalize(),
                t['fecha_inicio'],
                t['fecha_fin']
            ))
    
    def _filtrar_tratamientos(self):
        """Filtra los tratamientos por el paciente seleccionado"""
        seleccion = self.cb_paciente.get()
        if not seleccion:
            self._cargar_tabla()
            return
            
        try:
            paciente_id = int(seleccion.split(' - ')[0])
            self._cargar_tabla(paciente_id)
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Seleccione un paciente válido")
    
    def _abrir_formulario_tratamiento(self):
        """Abre un formulario para agregar un nuevo tratamiento"""
        if not self.pacientes:
            messagebox.showerror("Error", "No hay pacientes registrados")
            return
            
        formulario = tk.Toplevel(self)
        formulario.title("Nuevo Tratamiento")
        formulario.resizable(False, False)
        
        frame_principal = ttk.Frame(formulario)
        frame_principal.pack(pady=10, padx=10)
        
        ttk.Label(frame_principal, text="Paciente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        cb_paciente = ttk.Combobox(frame_principal, values=[f"{p['id_paciente']} - {p['nombre']}" for p in self.pacientes])
        cb_paciente.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame_principal, text="Nombre tratamiento:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame_principal)
        entry_nombre.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame_principal, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=5)
        text_descripcion = tk.Text(frame_principal, height=4, width=30)
        text_descripcion.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame_principal, text="Fecha inicio:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_fecha_inicio = ttk.Entry(frame_principal)
        entry_fecha_inicio.insert(0, datetime.now().strftime('%Y-%m-%d'))
        entry_fecha_inicio.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame_principal, text="Fecha fin:").grid(row=4, column=0, sticky=tk.W, pady=5)
        entry_fecha_fin = ttk.Entry(frame_principal)
        entry_fecha_fin.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame_principal, text="Estado:").grid(row=5, column=0, sticky=tk.W, pady=5)
        cb_estado = ttk.Combobox(frame_principal, values=['activo', 'pendiente'])
        cb_estado.set('activo')
        cb_estado.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        
        frame_botones = ttk.Frame(formulario)
        frame_botones.pack(pady=10)
        
        btn_guardar = ttk.Button(frame_botones, text="Guardar", command=lambda: self._guardar_tratamiento(
            formulario, cb_paciente.get(), entry_nombre.get(), text_descripcion.get("1.0", tk.END).strip(),
            entry_fecha_inicio.get(), entry_fecha_fin.get(), cb_estado.get()
        ))
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=formulario.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def _guardar_tratamiento(self, formulario, paciente, nombre, descripcion, fecha_inicio, fecha_fin, estado):
        """Guarda un nuevo tratamiento en la base de datos"""
        try:
            if not all([paciente, nombre, fecha_inicio, fecha_fin]):
                raise ValueError("Todos los campos obligatorios deben estar completos")
                
            paciente_id = int(paciente.split(' - ')[0])
            
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            
            if fecha_fin_dt < fecha_inicio_dt:
                raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
            
            datos = {
                'id_paciente': paciente_id,
                'nombre_tratamiento': nombre,
                'descripcion': descripcion,
                'estado': estado,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
            
            modelos.crear_tratamiento(datos)
            messagebox.showinfo("Éxito", "Tratamiento creado correctamente")
            formulario.destroy()
            self._cargar_tabla()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el tratamiento: {str(e)}")
    
    def _abrir_asignar_medicamento(self):
        """Abre la ventana para asignar un medicamento al tratamiento seleccionado"""
        seleccion = self.tabla.focus()
        if not seleccion:
            return
            
        tratamiento_id = self.tabla.item(seleccion)['values'][0]
        tratamiento_nombre = self.tabla.item(seleccion)['values'][2]
        
        from app.ui.asignar_medicamento import AsignarMedicamentoWindow
        AsignarMedicamentoWindow(self, tratamiento_id, tratamiento_nombre)
    
    def _habilitar_boton_asignar(self, event):
        """Habilita el botón de asignar medicamento cuando se selecciona un tratamiento"""
        seleccion = self.tabla.focus()
        self.btn_asignar['state'] = tk.NORMAL if seleccion else tk.DISABLED