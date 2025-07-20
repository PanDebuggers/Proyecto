import customtkinter as ctk

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Prueba CustomTkinter")
    app.geometry("400x200")

    label = ctk.CTkLabel(app, text="¡Funciona CustomTkinter!", font=("Helvetica", 16))
    label.pack(pady=40)

    app.mainloop()

if __name__ == "__main__":
    main()
