import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class RentaView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎟️ Registro de Rentas")
        self.geometry("850x500")

        # --- Formulario de renta ---
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="ID Renta:").grid(row=0, column=0)
        self.id_renta = tk.Entry(frame_form, width=10)
        self.id_renta.grid(row=0, column=1)

        tk.Label(frame_form, text="Cliente:").grid(row=0, column=2)
        self.cliente_entry = tk.Entry(frame_form, width=20)
        self.cliente_entry.grid(row=0, column=3)

        tk.Label(frame_form, text="Película:").grid(row=1, column=0)
        self.pelicula_entry = tk.Entry(frame_form, width=20)
        self.pelicula_entry.grid(row=1, column=1)

        tk.Label(frame_form, text="Fecha Renta:").grid(row=1, column=2)
        self.fecha_renta = tk.Entry(frame_form, width=15)
        self.fecha_renta.insert(0, date.today())
        self.fecha_renta.grid(row=1, column=3)

        tk.Label(frame_form, text="Fecha Límite:").grid(row=2, column=0)
        self.fecha_limite = tk.Entry(frame_form, width=15)
        self.fecha_limite.grid(row=2, column=1)

        tk.Label(frame_form, text="Fecha Devolución:").grid(row=2, column=2)
        self.fecha_devolucion = tk.Entry(frame_form, width=15)
        self.fecha_devolucion.grid(row=2, column=3)

        tk.Label(frame_form, text="Recargo: $").grid(row=3, column=0)
        self.recargo = tk.Entry(frame_form, width=10)
        self.recargo.grid(row=3, column=1)

        # --- Botones ---
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="💾 Registrar Renta", command=self.registrar_renta).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="📦 Registrar Devolución", command=self.registrar_devolucion).grid(row=0, column=1, padx=5)

        # --- Tabla de rentas ---
        columnas = ("ID", "Cliente", "Película", "F. Renta", "F. Límite")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tabla.heading(col, text=col)
        self.tabla.pack(pady=10)

    def registrar_renta(self): pass
    def registrar_devolucion(self): pass

if __name__ == "__main__":
    RentaView().mainloop()
