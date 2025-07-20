import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.ui.login import LoginView

from app.ui.base_view import iniciar_aplicacion  # Se importa la función de arranque

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MediCareDesk")
    root.state("zoomed")  # Inicia maximizado

    # Cargar la vista de login
    LoginView(master=root, on_login_success=lambda email: iniciar_aplicacion(email, root))

    root.mainloop()
