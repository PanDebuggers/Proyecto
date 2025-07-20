import tkinter as tk
import customtkinter as ctk

def mostrar_pacientes(frame_dinamico):
    for widget in frame_dinamico.winfo_children():
        widget.destroy()
    lbl = tk.Label(frame_dinamico, text="Listado de Pacientes", bg="#f0f0f0")
    lbl.pack(pady=50)