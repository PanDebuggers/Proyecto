import tkinter as tk
import customtkinter as ctk

def mostrar_medicamentos(frame_dinamico):
    for widget in frame_dinamico.winfo_children():
        widget.destroy()
    lbl = tk.Label(frame_dinamico, text="Vista de Medicamentos", bg="#f0f0f0")
    lbl.pack(pady=50)