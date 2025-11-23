import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class RentaView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎟️ Registro de Rentas")
        self.geometry("900x550")
        self.configure(bg="#E9EEF3")  # Fondo profesional claro

        # =======================
        #   HEADER SUPERIOR
        # =======================
        header = tk.Frame(self, bg="#2F3A56", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Sistema de Rentas • Películas",
            bg="#2F3A56",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        # =======================
        #   CARD FORMULARIO
        # =======================
        card = tk.Frame(self, bg="white", bd=0, relief="flat")
        card.pack(pady=15, padx=20, fill="x")

        tk.Label(card, text="Registrar Renta", bg="white",
                 font=("Segoe UI", 13, "bold"), fg="#2F3A56").grid(row=0, column=0, columnspan=4, pady=(10, 15))

        # Campos
        self._crear_label_entry(card, "Cliente:", 1, 0)
        self.cliente_entry = self._crear_entry(card, 1, 1, 20)

        self._crear_label_entry(card, "Película:", 1, 2)
        self.pelicula_entry = self._crear_entry(card, 1, 3, 20)

        self._crear_label_entry(card, "Fecha Renta:", 2, 0)
        self.fecha_renta = self._crear_entry(card, 2, 1, 15, date.today())

        self._crear_label_entry(card, "Fecha Límite:", 2, 2)
        self.fecha_limite = self._crear_entry(card, 2, 3, 15)

        self._crear_label_entry(card, "Fecha Devolución:", 3, 0)
        self.fecha_devolucion = self._crear_entry(card, 3, 1, 15)

        self._crear_label_entry(card, "Recargo: $", 3, 2)
        self.recargo = self._crear_entry(card, 3, 3, 10)

        # =======================
        #   BOTONES
        # =======================
        frame_btn = tk.Frame(self, bg="#E9EEF3")
        frame_btn.pack(pady=5)

        btn1 = tk.Button(frame_btn, text="💾 Registrar Renta",
                         bg="#E93E00", fg="white",
                         font=("Segoe UI", 11, "bold"),
                         relief="flat", padx=15, pady=6,
                         activebackground="#FF4000",
                         command=self.registrar_renta)
        btn1.grid(row=0, column=0, padx=10)

        btn2 = tk.Button(frame_btn, text="📦 Registrar Devolución",
                         bg="#07329E", fg="white",
                         font=("Segoe UI", 11, "bold"),
                         relief="flat", padx=15, pady=6,
                         activebackground="#0743BD",
                         command=self.registrar_devolucion)
        btn2.grid(row=0, column=1, padx=10)

        # =======================
        #   TABLA
        # =======================
        columnas = ("Cliente", "Película", "F. Renta", "F. Límite")

        tabla_frame = tk.Frame(self, bg="#E9EEF3")
        tabla_frame.pack(pady=10, fill="both", expand=True)

        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        # Estilo tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading",
                        background="#4B7EFF",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=25,
                        background="white",
                        fieldbackground="white")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")

        self.tabla.pack(fill="both", expand=True)

    # =======================
    #   HELPERS UI
    # =======================
    def _crear_label_entry(self, parent, texto, fila, col):
        tk.Label(parent, text=texto, bg="white",
                 font=("Segoe UI", 10, "bold"),
                 fg="#0048FF").grid(row=fila, column=col, sticky="e", padx=5, pady=5)

    def _crear_entry(self, parent, fila, col, ancho, valor_def=None):
        e = tk.Entry(parent, width=ancho, relief="solid", bd=1)
        if valor_def is not None:
            e.insert(0, valor_def)
        e.grid(row=fila, column=col, padx=5, pady=5)
        return e

    def registrar_renta(self):
        pass

    def registrar_devolucion(self):
        pass


if __name__ == "__main__":
    RentaView().mainloop()
