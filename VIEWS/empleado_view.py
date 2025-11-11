import tkinter as tk
from tkinter import ttk, messagebox

class EmpleadoView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Panel del Empleado - Catálogo de Películas")
        self.geometry("900x550")

        # --- Sección de búsqueda ---
        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(pady=10)
        tk.Label(frame_busqueda, text="🔍 Buscar película:").grid(row=0, column=0, padx=5)
        self.entry_busqueda = tk.Entry(frame_busqueda, width=50)
        self.entry_busqueda.grid(row=0, column=1, padx=5)
        tk.Button(frame_busqueda, text="Buscar", command=self.buscar_pelicula).grid(row=0, column=2, padx=5)

        # --- Tabla de películas ---
        columnas = ("ID", "Título", "Género", "Año", "Estado", "Precio")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tabla.heading(col, text=col)
        self.tabla.pack(pady=10, fill="x")

        # --- Botones de gestión ---
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="➕ Agregar", command=self.agregar).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="✏️ Editar", command=self.editar).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="🗑️ Eliminar", command=self.eliminar).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="🔄 Actualizar", command=self.actualizar).grid(row=0, column=3, padx=5)

        # --- Sección de rentas y devoluciones ---
        frame_rentas = tk.Frame(self)
        frame_rentas.pack(pady=15)
        tk.Button(frame_rentas, text="📋 Ver Rentas Activas", command=self.ver_rentas).grid(row=0, column=0, padx=20)
        tk.Button(frame_rentas, text="📦 Ver Devoluciones", command=self.ver_devoluciones).grid(row=0, column=1, padx=20)

        # --- Información del empleado ---
        frame_info = tk.Frame(self)
        frame_info.pack(side="bottom", fill="x", pady=10)
        tk.Label(frame_info, text="Empleado: Juliana Flores | Sesión activa", anchor="w").pack(fill="x") #nombre de empleado estático por ahora

    # Métodos (a conectar con los controladores)
    def buscar_pelicula(self): pass 
    def agregar(self): pass
    def editar(self): pass
    def eliminar(self): pass
    def actualizar(self): pass
    def ver_rentas(self): pass
    def ver_devoluciones(self): pass


if __name__ == "__main__":
    app = EmpleadoView()
    app.mainloop()
