import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.db import modelos
from app.logic import tratamientos as logic_tratamientos

class AsignarMedicamentoWindow(tk.Toplevel):
    def __init__(self, parent, tratamiento_id, tratamiento_nombre):
        super().__init__(parent)
        self.title(f"Asignar Medicamento - {tratamiento_nombre}")
        self.tratamiento_id = tratamiento_id
        self.tratamiento_nombre = tratamiento_nombre
        
        self.medicamentos = modelos.obtener_medicamentos()
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los elementos del formulario"""

        self.frame_principal = ttk.Frame(self)
        self.frame_principal.pack(pady=10, padx=10, fill=tk.BOTH)
        
        ttk.Label(self.frame_principal, text=f"Tratamiento: {self.tratamiento_nombre}", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        ttk.Label(self.frame_principal, text="Medicamento:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cb_medicamento = ttk.Combobox(
            self.frame_principal, 
            values=[f"{m['id_medicamento']} - {m['nombre']}" for m in self.medicamentos]
        )
        self.cb_medicamento.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Dosis:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_dosis = ttk.Entry(self.frame_principal)
        self.entry_dosis.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Frecuencia:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cb_frecuencia = ttk.Combobox(
            self.frame_principal,
            values=[
                'una_vez_al_dia',
                'cada_8_horas',
                'cada_12_horas',
                'cada_24_horas',
                'personalizada'
            ]
        )
        self.cb_frecuencia.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Vía de administración:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cb_via = ttk.Combobox(
            self.frame_principal,
            values=[
                'oral',
                'intravenosa',
                'topica',
                'intramuscular',
                'subcutanea',
                'inhalatoria',
                'rectal',
                'sublingual',
                'oftalmologica',
                'otica',
                'nasal',
                'transdermica'
            ]
        )
        self.cb_via.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Hora preferida (HH:MM):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_hora = ttk.Entry(self.frame_principal)
        self.entry_hora.insert(0, "08:00")
        self.entry_hora.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Fecha inicio (opcional):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.entry_fecha_inicio = ttk.Entry(self.frame_principal)
        self.entry_fecha_inicio.grid(row=6, column=1, sticky=tk.EW, pady=5, padx=5)
        

        ttk.Label(self.frame_principal, text="Fecha fin (opcional):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.entry_fecha_fin = ttk.Entry(self.frame_principal)
        self.entry_fecha_fin.grid(row=7, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(self.frame_principal, text="Estado:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.cb_estado = ttk.Combobox(
            self.frame_principal,
            values=['activo', 'suspendido', 'pendiente']
        )
        self.cb_estado.set('activo')
        self.cb_estado.grid(row=8, column=1, sticky=tk.EW, pady=5, padx=5)
        
        self.frame_botones = ttk.Frame(self)
        self.frame_botones.pack(pady=10)
        
        btn_guardar = ttk.Button(self.frame_botones, text="Guardar", command=self._guardar_asignacion)
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = ttk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def _guardar_asignacion(self):
        """Guarda la asignación del medicamento al tratamiento"""
        try:

            medicamento_str = self.cb_medicamento.get()
            if not medicamento_str:
                raise ValueError("Debe seleccionar un medicamento")
            
            medicamento_id = int(medicamento_str.split(' - ')[0])
            
            hora_preferida = self.entry_hora.get()
            try:
                datetime.strptime(hora_preferida, '%H:%M')
            except ValueError:
                raise ValueError("Formato de hora inválido. Use HH:MM")
            
            fecha_inicio = self.entry_fecha_inicio.get() or None
            fecha_fin = self.entry_fecha_fin.get() or None
            
            if fecha_inicio:
                datetime.strptime(fecha_inicio, '%Y-%m-%d')
            if fecha_fin:
                datetime.strptime(fecha_fin, '%Y-%m-%d')
            
            datos = {
                'id_tratamiento': self.tratamiento_id,
                'id_medicamento': medicamento_id,
                'dosis': self.entry_dosis.get(),
                'frecuencia': self.cb_frecuencia.get(),
                'via_administracion': self.cb_via.get(),
                'hora_preferida': hora_preferida,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'estado': self.cb_estado.get()
            }
            
            if not all([datos['frecuencia'], datos['via_administracion'], datos['estado']]):
                raise ValueError("Todos los campos obligatorios deben estar completos")
            
            asignacion_id = logic_tratamientos.asignar_medicamento_a_tratamiento(**datos)
            
            logic_tratamientos.generar_tomas_tratamiento(asignacion_id)
            
            messagebox.showinfo("Éxito", "Medicamento asignado correctamente y tomas generadas")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo asignar el medicamento: {str(e)}")