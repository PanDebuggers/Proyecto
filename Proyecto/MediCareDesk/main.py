import tkinter as tk
from app.ui.login import LoginView
from app.ui.menu_lateral import MenuLateral  # Vista principal con nombre del cuidador
from app import session

def iniciar_aplicacion(correo_usuario):
    # Cerramos la ventana de login
    for widget in root.winfo_children():
        widget.destroy()

    # Mostramos la vista principal (con menú lateral, etc.)
    MenuLateral(root).pack(fill="both", expand=True)

root = tk.Tk()
root.geometry("800x600")
root.title("MediCareDesk")

# Iniciamos con la vista de login
login_view = LoginView(master=root, on_login_success=iniciar_aplicacion)
login_view.pack(fill="both", expand=True)

root.mainloop()
