import sys
import os
<<<<<<< Updated upstream
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))  # Agrega la raíz del proyecto
from app import session
=======
>>>>>>> Stashed changes
import tkinter as tk
import customtkinter as ctk

# Agrega la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app import session


class MenuLateral(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.sidebar = None  # Se inicializa el atributo sidebar
        self.mostrar_usuario()

    def mostrar_usuario(self):
        cuidador = session.cuidador_actual
        if cuidador:
            nombre = cuidador["nombre"]
            return nombre
        return "Sin usuario"

    def crear_sidebar(self, ventana):
<<<<<<< Updated upstream
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
=======
        # Barra lateral
        self.sidebar = tk.Frame(ventana, width=200, bg="#d3d3d3")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Icono
        IMG_PATH = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "resources", "iconos", "MediCareDesk_Logo_125x125.png"
        )
        IMG_PATH = os.path.abspath(IMG_PATH)

        icono = tk.PhotoImage(file=IMG_PATH)
        icono_label = tk.Label(self.sidebar, image=icono, bg="#d3d3d3")
        icono_label.image = icono  # Evita que la imagen se elimine por el recolector de basura
        icono_label.pack(pady=20)

        # Botones de la barra lateral
        self.btn_pacientes = ctk.CTkButton(self.sidebar, text="Pacientes", corner_radius=20, anchor="w")
        self.btn_pacientes.pack(fill=tk.X, padx=10, pady=5)

        self.btn_medicamentos = ctk.CTkButton(self.sidebar, text="Medicamentos", corner_radius=20, anchor="w")
        self.btn_medicamentos.pack(fill=tk.X, padx=10, pady=5)

        self.btn_tratamientos = ctk.CTkButton(self.sidebar, text="Tratamientos", corner_radius=20, anchor="w")
        self.btn_tratamientos.pack(fill=tk.X, padx=10, pady=5)

        self.btn_tomas_dia = ctk.CTkButton(
            self.sidebar, text="Tomas del día", corner_radius=20, anchor="w", command=self.on_tomas_dia
        )
        self.btn_tomas_dia.pack(fill=tk.X, padx=10, pady=5)

        self.btn_historial_tomas = ctk.CTkButton(
            self.sidebar, text="Historial de tomas", corner_radius=20, anchor="w", command=self.on_historial_tomas
        )
        self.btn_historial_tomas.pack(fill=tk.X, padx=10, pady=5)

        self.btn_alertas = ctk.CTkButton(
            self.sidebar, text="🔔 Alertas", corner_radius=20, anchor="w", command=self.on_alertas
        )
        self.btn_alertas.pack(fill="x", padx=10, pady=5)

    def on_alertas(self):
        from app.ui.alertas import mostrar_alertas

        parent = self.master
        frame_dinamico = None
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame) and child.cget("bg") == "#f0f0f0":
                frame_dinamico = child
                break
        if frame_dinamico:
            id_cuidador = session.cuidador_actual["id_cuidador"]
            mostrar_alertas(frame_dinamico, id_cuidador)
        else:
            print("No se encontró el frame dinámico para mostrar las alertas.")

        # Espacio expansor
        espaciador = tk.Label(self.sidebar, text="", bg="#d3d3d3")
>>>>>>> Stashed changes
        espaciador.pack(expand=True)

        frame_usuario = tk.Frame(self.sidebar, bg="#d3d3d3")
        frame_usuario.pack(fill="x", padx=10, pady=10)

<<<<<<< Updated upstream
        #nombre_usuario = get_usuario()
=======
>>>>>>> Stashed changes
        nombre_usuario = self.mostrar_usuario()
        lbl_usuario = tk.Label(frame_usuario, text=f"🧑 {nombre_usuario}", bg="#d3d3d3")
        lbl_usuario.pack(anchor="w")

<<<<<<< Updated upstream
        self.btn_logout = ctk.CTkButton(sidebar, text="🔓 Cerrar sesión", corner_radius=20, anchor="w")
=======
        self.btn_logout = ctk.CTkButton(self.sidebar, text="🔓 Cerrar sesión", corner_radius=20, anchor="w")
>>>>>>> Stashed changes
        self.btn_logout.pack(fill="x", padx=10, pady=5)

    def on_tomas_dia(self):
<<<<<<< Updated upstream
        # Aquí va la lógica para mostrar tomas del día
        print("Mostrar Tomas del día")

    def on_historial_tomas(self):
        # Aquí va la lógica para mostrar historial de tomas
        print("Mostrar Historial de tomas")
=======
        from app.ui.tomas import mostrar_tomas_dia

        parent = self.master
        frame_dinamico = None
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame) and child.cget("bg") == "#f0f0f0":
                frame_dinamico = child
                break
        if frame_dinamico:
            id_cuidador = session.cuidador_actual["id_cuidador"]
            mostrar_tomas_dia(frame_dinamico, id_cuidador)
        else:
            print("No se encontró el frame dinámico para mostrar las tomas del día.")

    def on_historial_tomas(self):
        from app.ui.historial_tomas import mostrar_historial_tomas
        from app.db import modelos

        parent = self.master
        frame_dinamico = None
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame) and child.cget("bg") == "#f0f0f0":
                frame_dinamico = child
                break
        if frame_dinamico:
            id_cuidador = session.cuidador_actual["id_cuidador"]
            pacientes = modelos.obtener_pacientes()
            pacientes_cuidador = [p for p in pacientes if p["id_cuidador"] == id_cuidador]

            if not pacientes_cuidador:
                tk.Label(
                    frame_dinamico, text="No hay pacientes registrados.",
                    bg="#f0f0f0", fg="gray"
                ).pack(pady=20)
                return

            def seleccionar_paciente():
                seleccion = lista.curselection()
                if not seleccion:
                    return
                idx = seleccion[0]
                paciente = pacientes_cuidador[idx]
                mostrar_historial_tomas(frame_dinamico, paciente["id_paciente"], paciente["nombre"])

            for widget in frame_dinamico.winfo_children():
                widget.destroy()

            tk.Label(frame_dinamico, text="Seleccione un paciente:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
            lista = tk.Listbox(frame_dinamico, font=("Arial", 12), height=8)
            for p in pacientes_cuidador:
                lista.insert(tk.END, p["nombre"])
            lista.pack(pady=10)
            btn = tk.Button(frame_dinamico, text="Ver historial", command=seleccionar_paciente)
            btn.pack(pady=5)
        else:
            print("No se encontró el frame dinámico para mostrar el historial de tomas.")
>>>>>>> Stashed changes
