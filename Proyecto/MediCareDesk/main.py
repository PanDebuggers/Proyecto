# main.py

import tkinter as tk
from app.ui.login import LoginView
from app.ui.menu_lateral import MenuLateral

def iniciar_aplicacion(correo_usuario):
    for widget in root.winfo_children():
        widget.destroy()
    MenuLateral(root, correo_usuario).pack(fill="both", expand=True)

root = tk.Tk()
root.title("MediCareDesk")
root.state("zoomed")  # Inicia maximizado

# Vista inicial: login
LoginView(master=root, on_login_success=iniciar_aplicacion)

root.mainloop()
