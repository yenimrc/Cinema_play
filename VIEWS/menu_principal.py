# VIEWS/menu_principal.py

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración principal
        self.title("CINEMA PLAY - Sistema de Gestión")
        self.geometry("940x620")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        # Centrar
        self.center_window()

        # Estilos
        self.setup_styles()

        # Construir interfaz
        self.create_layout()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Botón principal
        style.configure(
            "Primary.TButton",
            background="#ff4747",
            foreground="white",
            font=("Segoe UI", 12, "bold"),
            padding=15,
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#e33e3e"), ("pressed", "#c93636")]
        )

        # Botones secundarios
        style.configure(
            "Secondary.TButton",
            background="#007fff",
            foreground="white",
            font=("Segoe UI", 11, "bold"),
            padding=13,
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#006ada"), ("pressed", "#005bbd")]
        )

    def create_layout(self):

        # Barra superior con gradiente
        header = tk.Canvas(self, height=90, bd=0, highlightthickness=0)
        header.pack(fill="x")

        # Gradiente horizontal vivo
        self.draw_gradient(header, "#ff5f6d", "#ffc371")

        tk.Label(
            header,
            text="🎬  CINEMA PRO",
            font=("Segoe UI", 30, "bold"),
            bg="",
            fg="white"
        ).place(x=30, y=20)

        # Contenedor principal
        content = tk.Frame(self, bg="#f0f2ff")
        content.pack(fill="both", expand=True)

        # Tarjetas estadísticas
        self.create_stats_cards(content)

        # Botones de acción grandes
        self.create_action_buttons(content)

    def draw_gradient(self, canvas, color1, color2):
        width = 940
        for i in range(width):
            ratio = i / width
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            canvas.create_line(i, 0, i, 200, fill=f"#{r:02x}{g:02x}{b:02x}")

    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    def create_stats_cards(self, parent):
        frame = tk.Frame(parent, bg="#f0f2ff")
        frame.pack(pady=20)

        stats = [
            ("🎞️ Películas", "156", "#fa0000"),
            ("🎟️ Salas", "12", "#ff9f1c"),
            ("👥 Usuarios", "2400", "#005dba"),
            ("📅 Hoy", "342", "#00da24"),
        ]

        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(frame, bg="white", width=180, height=110, bd=0)
            card.grid(row=0, column=i, padx=15)
            card.pack_propagate(False)

            tk.Label(card, text=value, font=("Segoe UI", 26, "bold"), fg=color, bg="white").pack()
            tk.Label(card, text=title, font=("Segoe UI", 11), fg="#444", bg="white").pack()

    def create_action_buttons(self, parent):
        frame = tk.Frame(parent, bg="#f0f2ff")
        frame.pack(pady=40)

        ttk.Button(
            frame,
            text="🎬  EXPLORAR CATÁLOGO",
            style="Primary.TButton",
            command=self.abrir_cliente
        ).grid(row=0, column=0, padx=20, pady=15, ipadx=15, ipady=10)

        ttk.Button(
            frame,
            text="🔐  PANEL ADMINISTRATIVO",
            style="Secondary.TButton",
            command=self.abrir_empleado
        ).grid(row=0, column=1, padx=20, pady=15, ipadx=15, ipady=10)

        ttk.Button(
            frame,
            text="⚙️  CONFIGURACIÓN",
            style="Secondary.TButton",
            command=self.mostrar_configuracion
        ).grid(row=1, column=0, padx=20, pady=15, ipadx=15, ipady=10)

        ttk.Button(
            frame,
            text="📊  REPORTES",
            style="Secondary.TButton",
            command=self.mostrar_reportes
        ).grid(row=1, column=1, padx=20, pady=15, ipadx=15, ipady=10)

    def abrir_cliente(self):
        try:
            from VIEWS.cliente_view import CatalogoPeliculasView
            self.withdraw()
            ventana = CatalogoPeliculasView(self)
            ventana.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la vista cliente: {e}")

    def abrir_empleado(self):
        try:
            from VIEWS.empleado_view import EmpleadoView
            self.withdraw()
            ventana = EmpleadoView(self)
            ventana.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la vista administrador: {e}")

    def mostrar_configuracion(self):
        messagebox.showinfo("Administrador", "Vista de administrador no implementada.")

    def mostrar_configuracion(self):
        messagebox.showinfo("Configuración", "Panel de configuración.")

    def mostrar_reportes(self):
        messagebox.showinfo("Reportes", "Panel de reportes.")

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()


