import tkinter as tk
from tkinter import ttk, messagebox

class PeliculaView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Gestión de Películas")
        self.geometry("900x540")
        self.configure(bg="#F2F6FF")

        # ========== HEADER ==========
        header = tk.Frame(self, bg="#1F6FEB", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Gestión de Películas",
            bg="#1F6FEB",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # ========== CARD FORMULARIO ==========
        card = tk.Frame(self, bg="white", bd=0, padx=10, pady=10)
        card.pack(pady=15, padx=25, fill="x")

        tk.Label(
            card,
            text="Registrar / Editar Película",
            bg="white",
            fg="#0D2B60",
            font=("Segoe UI", 15, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=(5, 20))

        # ---------- TÍTULO ----------
        tk.Label(
            card, text="Título:", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=0, sticky="e", padx=5)

        self.titulo_entry = tk.Entry(
            card, width=35, relief="flat",
            highlightthickness=2, highlightbackground="#1F6FEB"
        )
        self.titulo_entry.grid(row=1, column=1, padx=5, pady=5)

        # ---------- GÉNERO ----------
        tk.Label(
            card, text="Género:", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=2, sticky="e", padx=5)

        self.genero_combo = ttk.Combobox(
            card,
            values=[
                "Acción", "Aventura", "Comedia", "Drama", "Romance",
                "Terror", "Ciencia Ficción", "Suspenso", "Animación",
                "Documental"
            ],
            width=20
        )
        self.genero_combo.grid(row=1, column=3, padx=5, pady=5)

        # ---------- ESTADO ----------
        tk.Label(
            card, text="Estado:", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=2, column=0, sticky="e", padx=5)

        self.estado_combo = ttk.Combobox(
            card,
            values=["Disponible", "Rentada"],
            width=20
        )
        self.estado_combo.grid(row=2, column=1, padx=5, pady=5)

        # ========== BOTONES ==========
        frame_btn = tk.Frame(self, bg="#F2F6FF")
        frame_btn.pack(pady=10)

        botones = [
            ("➕ Agregar", "#FF6200", "#FF6600", self.agregar),
            ("✏️ Editar", "#0066FF", "#0059FF", self.editar),
            ("🗑️ Eliminar", "#FF0000", "#FF0000", self.eliminar),
            ("🔍 Buscar", "#FFBF00", "#FFC002", self.buscar)
        ]

        for i, (txt, bg, hover, cmd) in enumerate(botones):
            btn = tk.Button(
                frame_btn, text=txt, bg=bg, fg="white",
                font=("Segoe UI", 11, "bold"),
                relief="flat", padx=20, pady=7,
                activebackground=hover,
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=0, column=i, padx=12)

        # ========== TABLA ==========
        columnas = ("Título", "Género", "Estado")

        tabla_frame = tk.Frame(self, bg="#F2F6FF")
        tabla_frame.pack(pady=10, fill="both", expand=True)

        self.tabla = ttk.Treeview(
            tabla_frame, columns=columnas,
            show="headings", height=10
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading",
                        background="#004AB9",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=27,
                        background="white",
                        fieldbackground="white")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200, anchor="center")

        self.tabla.pack(fill="both", expand=True)

    # ========== FUNCIONES ==========
    def agregar(self): pass
    def editar(self): pass
    def eliminar(self): pass
    def buscar(self): pass


if __name__ == "__main__":
    PeliculaView().mainloop()
