import tkinter as tk
from app.ui.login import LoginView
from app.ui.menu_lateral import MenuLateral  # Si ya lo tienes
from app import session

def iniciar_aplicacion(correo_usuario):
    for widget in root.winfo_children():
        widget.destroy()
    MenuLateral(root).pack(fill="both", expand=True)

root = tk.Tk()
root.title("MediCareDesk")
root.state("zoomed")  # ← Pantalla maximizada al iniciar (solo en Windows)

login_view = LoginView(master=root, on_login_success=iniciar_aplicacion)
login_view.pack(fill="both", expand=True)

root.mainloop()
