import tkinter as tk
from tkinter import ttk, messagebox

class PeliculaView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Gestión de Películas")
        self.geometry("800x500")

        # --- Campos de entrada ---
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0)
        self.id_entry = tk.Entry(frame_form, width=10)
        self.id_entry.grid(row=0, column=1)

        tk.Label(frame_form, text="Título:").grid(row=0, column=2)
        self.titulo_entry = tk.Entry(frame_form, width=25)
        self.titulo_entry.grid(row=0, column=3)

        tk.Label(frame_form, text="Género:").grid(row=1, column=0)
        self.genero_entry = tk.Entry(frame_form, width=15)
        self.genero_entry.grid(row=1, column=1)

        tk.Label(frame_form, text="Año:").grid(row=1, column=2)
        self.anio_entry = tk.Entry(frame_form, width=10)
        self.anio_entry.grid(row=1, column=3)

        tk.Label(frame_form, text="Estado:").grid(row=2, column=0)
        self.estado_combo = ttk.Combobox(frame_form, values=["Disponible", "Rentada"])
        self.estado_combo.grid(row=2, column=1)

        # --- Botones ---
        frame_btn = tk.Frame(self)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="➕ Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="✏️ Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="🗑️ Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="🔍 Buscar", command=self.buscar).grid(row=0, column=3, padx=5)

        # --- Tabla ---
        columnas = ("ID", "Título", "Género", "Año", "Estado")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tabla.heading(col, text=col)
        self.tabla.pack(pady=10)

    def agregar(self): pass
    def editar(self): pass
    def eliminar(self): pass
    def buscar(self): pass

if __name__ == "__main__":
    PeliculaView().mainloop()
