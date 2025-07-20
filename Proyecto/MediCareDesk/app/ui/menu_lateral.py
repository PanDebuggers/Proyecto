import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))  # Agrega la raíz del proyecto
from app import session
import tkinter as tk
import customtkinter as ctk
from app import session


class MenuLateral(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.mostrar_usuario()

    def mostrar_usuario(self):
        cuidador = session.cuidador_actual
        if cuidador:
            nombre = cuidador["nombre"]
            return nombre
        return "Sin usuario"

    def crear_sidebar(self, ventana):
        #Barra lateral
        sidebar = tk.Frame(ventana, width=200, bg="#d3d3d3")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        #Icono
        IMG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "iconos", "MediCareDesk_Logo_125x125.png")
        IMG_PATH = os.path.abspath(IMG_PATH)

        icono = tk.PhotoImage(file=IMG_PATH)
        icono_label = tk.Label(sidebar, image=icono, bg="#d3d3d3")
        icono_label.image = icono  # Evita que la imagen se elimine por el recolector de basura
        icono_label.pack(pady=20)

        #Botones de la barra lateral
        self.btn_pacientes = ctk.CTkButton(sidebar, text="Pacientes", corner_radius=20, anchor="w")
        self.btn_pacientes.pack(fill=tk.X, padx=10, pady=5)

        self.btn_medicamentos = ctk.CTkButton(sidebar, text="Medicamentos", corner_radius=20, anchor="w")
        self.btn_medicamentos.pack(fill=tk.X, padx=10, pady=5)

        self.btn_tratamientos = ctk.CTkButton(sidebar, text="Tratamientos", corner_radius=20, anchor="w")
        self.btn_tratamientos.pack(fill=tk.X, padx=10, pady=5)

        #submenu tomas
        tomas_menu_btn = tk.Menubutton(
        sidebar,
        text="Tomas",
        bg="#d3d3d3",           # Mismo color que los botones
        fg="black",             # Color del texto
        font=("Arial", 12),     # Fuente igual que los botones
        anchor="w",
        relief="raised",
        activebackground="#c0c0c0",  # Color al pasar el mouse
        activeforeground="black"
        )
        tomas_menu_btn.pack(fill=tk.X, padx=10, pady=15)

        tomas_menu = tk.Menu(tomas_menu_btn, tearoff=0)
        tomas_menu.add_command(label="Tomas del día", command=self.on_tomas_dia)
        tomas_menu.add_command(label="Historial de tomas", command=self.on_historial_tomas)
        tomas_menu_btn.config(menu=tomas_menu)

        #Alertas
        self.btn_alertas = ctk.CTkButton(sidebar, text="🔔 Alertas", corner_radius=20, anchor="w")
        self.btn_alertas.pack(fill="x", padx=10, pady=5)

        # Espacio expansor para empujar info de usuario abajo
        espaciador = tk.Label(sidebar, text="", bg="#d3d3d3")
        espaciador.pack(expand=True)

        frame_usuario = tk.Frame(sidebar, bg="#d3d3d3")
        frame_usuario.pack(fill="x", padx=10, pady=10)

        #nombre_usuario = get_usuario()
        nombre_usuario = self.mostrar_usuario()
        lbl_usuario = tk.Label(frame_usuario, text=f"🧑 {nombre_usuario}", bg="#d3d3d3")
        lbl_usuario.pack(anchor="w")

        self.btn_logout = ctk.CTkButton(sidebar, text="🔓 Cerrar sesión", corner_radius=20, anchor="w")
        self.btn_logout.pack(fill="x", padx=10, pady=5)

    # Funciones de los botones del menú
    def on_tomas_dia(self):
        # Aquí va la lógica para mostrar tomas del día
        print("Mostrar Tomas del día")

    def on_historial_tomas(self):
        # Aquí va la lógica para mostrar historial de tomas
        print("Mostrar Historial de tomas")