import tkinter as tk
from tkinter import ttk, messagebox

class CatalogoPeliculasView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Catálogo de Películas")
        self.geometry("800x500")

        # Campo de búsqueda
        tk.Label(self, text="🔍 Buscar película:").pack(pady=5)
        self.entry_busqueda = tk.Entry(self, width=50)
        self.entry_busqueda.pack()
        tk.Button(self, text="Buscar", command=self.buscar_pelicula).pack(pady=5)

        # Tabla de películas
        columnas = ("ID", "Título", "Género", "Estado")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tabla.heading(col, text=col)
        self.tabla.pack(pady=10)

        # Botones de acción
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="🎟️ Rentar", command=self.rentar).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="📦 Devolver", command=self.devolver).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="🔄 Actualizar Catálogo", command=self.actualizar).grid(row=0, column=2, padx=5)

    def buscar_pelicula(self):
        pass  # Aquí se conecta con pelicula_controller

    def rentar(self):
        pass  # Aquí se conecta con renta_controller

    def devolver(self):
        pass  # Aquí se conecta con renta_controller

    def actualizar(self):
        pass  # Aquí se conecta con pelicula_controller

if __name__ == "__main__":
    app = CatalogoPeliculasView()
    app.mainloop()
