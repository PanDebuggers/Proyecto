import tkinter as tk
import customtkinter as ctk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.ui.menu_lateral import MenuLateral
from app.ui.pacientes import mostrar_pacientes
from app.ui.medicamentos import mostrar_medicamentos
from app.ui.tratamientos import mostrar_tratamientos
from app.ui.login import LoginView
from app import session


def mostrar_login(root):
    for widget in root.winfo_children():
        widget.destroy()
    LoginView(master=root, on_login_success=lambda email: iniciar_aplicacion(email, root))


def iniciar_aplicacion(email, root):
    print(f"Iniciando aplicación. Usuario: {email}")
    for widget in root.winfo_children():
        widget.destroy()

    frame_principal = tk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True)

    # Menú lateral
    menu_lateral = MenuLateral(frame_principal)
    menu_lateral.crear_sidebar(frame_principal)

    # Contenido central
    frame_derecho = tk.Frame(frame_principal)
    frame_derecho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_dinamico = tk.Frame(frame_derecho, bg="#f0f0f0", bd=2, relief="groove")
    frame_dinamico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    img_path = os.path.abspath("resources/iconos/MediCareDesk_Logo_255x255.png")
    if os.path.exists(img_path):
        imagen_defecto = tk.PhotoImage(file=img_path)
        lbl_imagen = tk.Label(frame_dinamico, image=imagen_defecto, bg="#f0f0f0")
        lbl_imagen.image = imagen_defecto
        lbl_imagen.pack(expand=True)
    else:
        tk.Label(frame_dinamico, text="Bienvenido a MediCareDesk", bg="#f0f0f0", font=("Arial", 16)).pack(expand=True)

    frame_alertas = tk.Frame(frame_derecho, bg="#f0f0f0", highlightbackground="black", highlightthickness=2)
    frame_alertas.pack(side=tk.BOTTOM, fill=tk.X)

    lbl_alerta = tk.Label(frame_alertas, text="Sin alertas", bg="#f0f0f0", fg="red", font=("Arial", 12))
    lbl_alerta.pack(pady=5)

    # ✅ Toma el id del cuidador logueado desde session
    cuidador_actual = session.cuidador_actual
    id_cuidador = cuidador_actual["id_cuidador"]

    # Asignar funcionalidad a los botones
    menu_lateral.btn_pacientes.configure(command=lambda: mostrar_pacientes(frame_dinamico, id_cuidador))
    menu_lateral.btn_medicamentos.configure(command=lambda: mostrar_medicamentos(frame_dinamico))
    menu_lateral.btn_tratamientos.configure(command=lambda: mostrar_tratamientos(frame_dinamico))
    menu_lateral.btn_logout.configure(command=lambda: mostrar_login(root))

