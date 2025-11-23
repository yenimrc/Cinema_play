import tkinter as tk
from tkinter import ttk, messagebox

class EmpleadoView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Panel del Empleado - Catálogo de Películas")
        self.geometry("900x550")
        self.configure(bg='#f5f5f5')

        # --- Sección de búsqueda ---
        frame_busqueda = tk.Frame(self, bg='#f5f5f5')
        frame_busqueda.pack(pady=15)
        
        tk.Label(frame_busqueda, 
                text="🔍 Buscar película:", 
                bg='#f5f5f5',
                fg='#1565c0',
                font=('Arial', 11, 'bold')).grid(row=0, column=0, padx=5)
        
        self.entry_busqueda = tk.Entry(frame_busqueda, 
                                     width=50, 
                                     font=('Arial', 11),
                                     bg='#e3f2fd',
                                     fg='#0d47a1',
                                     insertbackground='#1565c0')
        self.entry_busqueda.grid(row=0, column=1, padx=5)
        
        tk.Button(frame_busqueda, 
                 text="Buscar", 
                 command=self.buscar_pelicula,
                 bg='#2196f3',
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15).grid(row=0, column=2, padx=5)

        # --- Tabla de películas ---
        columnas = ("Título", "Género", "Estado", "Precio")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        
        # Configurar estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#e3f2fd",
                       foreground="#0d47a1",
                       fieldbackground="#e3f2fd",
                       font=('Arial', 10))
        
        style.configure("Treeview.Heading", 
                       background="#1976d2",
                       foreground="black",
                       font=('Arial', 11, 'bold'))
        
        for col in columnas:
            self.tabla.heading(col, text=col)
        
        self.tabla.pack(pady=10, fill="x", padx=20)

        # --- Botones de gestión ---
        frame_botones = tk.Frame(self, bg='#f5f5f5')
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, 
                 text="➕ Agregar", 
                 command=self.agregar,
                 bg="#00a616",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=0, padx=8)
        
        tk.Button(frame_botones, 
                 text="✏️ Editar", 
                 command=self.editar,
                 bg="#ffc400",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=1, padx=8)
        
        tk.Button(frame_botones, 
                 text="🗑️ Eliminar", 
                 command=self.eliminar,
                 bg="#e30404",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=2, padx=8)
        
        tk.Button(frame_botones, 
                 text="🔄 Actualizar", 
                 command=self.actualizar,
                 bg="#005ac0",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=3, padx=8)

        # --- Sección de rentas y devoluciones ---
        frame_rentas = tk.Frame(self, bg='#f5f5f5')
        frame_rentas.pack(pady=15)
        
        tk.Button(frame_rentas, 
                 text="📋 Ver Rentas Activas", 
                 command=self.ver_rentas,
                 bg="#1588e6",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=20,
                 pady=5).grid(row=0, column=0, padx=15)
        
        tk.Button(frame_rentas, 
                 text="📦 Ver Devoluciones", 
                 command=self.ver_devoluciones,
                 bg="#56b3ff",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=20,
                 pady=5).grid(row=0, column=1, padx=15)

        # --- Información del empleado ---
        frame_info = tk.Frame(self, bg='#bbdefb')
        frame_info.pack(side="bottom", fill="x", pady=10)
        
        tk.Label(frame_info, 
                text="Empleado: Juliana Flores | Sesión activa", 
                anchor="w",
                bg='#bbdefb',
                fg='#0d47a1',
                font=('Arial', 10, 'bold')).pack(fill="x", padx=20, pady=8)

    # Métodos (a conectar con los controladores)
    def buscar_pelicula(self): 
        pass 
    def agregar(self): 
        pass
    def editar(self): 
        pass
    def eliminar(self): 
        pass
    def actualizar(self): 
        pass
    def ver_rentas(self): 
        pass
    def ver_devoluciones(self): 
        pass


if __name__ == "__main__":
    app = EmpleadoView()
    app.mainloop()