import tkinter as tk
from tkinter import ttk, messagebox

class CatalogoPeliculasView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 CINEMA PLAY - Catálogo de Películas")
        self.geometry("900x600")
        self.configure(bg='#f4f4f9')  # Fondo claro
        
        # Configurar estilo para widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.crear_interfaz()
    
    def configure_styles(self):
        """Configurar estilos personalizados para los widgets"""
        self.style.configure('Titulo.TLabel', 
                           background='#f4f4f9', 
                           foreground="#8fa6cb", 
                           font=('Georgia', 20, 'bold'))
        
        # Botones con colores distintos
        self.style.configure('Buscar.TButton',
                           background="#1e5abb",  # Azul
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Rentar.TButton',
                           background="#0492cf",  # Azul clario
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Devolver.TButton',
                           background="#1c66dc",  # azul
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Actualizar.TButton',
                           background="#afafc5",  # Gris neutro
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        # Tabla
        self.style.configure('Custom.Treeview',
                           background='#ffffff',
                           foreground='#222222',
                           fieldbackground='#ffffff',
                           font=('Verdana', 10))
        
        self.style.configure('Custom.Treeview.Heading',
                           background="#5b76a1",    #color de fondo de encabezados de tabla
                           foreground='black',      #color de texto de encabezados de tabla
                           font=('Verdana', 11, 'bold'))
        
        self.style.configure('Entry.TEntry',
                           fieldbackground='#ffffff',
                           foreground='#222222',
                           insertcolor="#0a5ce0")
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self, bg='#f4f4f9')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título principal centrado
        titulo = tk.Label(main_frame, 
                         text="🎬 CINEMA PLAY", 
                         font=('Georgia', 22, 'bold'),
                         bg='#f4f4f9',
                         fg="#000000")
        titulo.pack(pady=(0, 20))
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(main_frame, bg='#f4f4f9')
        frame_busqueda.pack(pady=(0, 15))
        
        tk.Label(frame_busqueda, 
                text="🔍 Nombre de Película:", 
                font=('Calibri', 12, 'bold'),
                bg="#1e5ec4", 
                fg="#000000").grid(row=0, column=0, padx=10)
        
        self.entry_busqueda = ttk.Entry(frame_busqueda, 
                                      width=40, 
                                      style='Entry.TEntry',
                                      font=('Verdana', 11))
        self.entry_busqueda.grid(row=0, column=1, padx=10)
    
        btn_buscar = ttk.Button(frame_busqueda, 
                              text="Buscar", 
                              command=self.buscar_pelicula,
                              style='Buscar.TButton')
        btn_buscar.grid(row=0, column=2, padx=10)
        
        # Frame de la tabla
        frame_tabla = tk.Frame(main_frame, bg="#000000")
        frame_tabla.pack(fill='both', expand=True, pady=(0, 15))
    
        columnas = ("Título", "Género", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, 
                                columns=columnas, 
                                show="headings", 
                                height=12,
                                style='Custom.Treeview')
        
        self.tabla.heading("Título", text="🎭 TÍTULO")
        self.tabla.heading("Género", text="🎪 GÉNERO")
        self.tabla.heading("Estado", text="📊 ESTADO")
        
        self.tabla.column("Título", width=300, anchor='center')
        self.tabla.column("Género", width=200, anchor='center')
        self.tabla.column("Estado", width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.agregar_datos_ejemplo()
        
        # Frame de botones de acción
        frame_botones = tk.Frame(main_frame, bg='#f4f4f9')
        frame_botones.pack(pady=10)
        
        btn_rentar = ttk.Button(frame_botones, 
                              text="🎟️ RENTAR PELÍCULA", 
                              command=self.rentar,
                              style='Rentar.TButton')
        btn_rentar.grid(row=0, column=0, padx=10)
        
        btn_devolver = ttk.Button(frame_botones, 
                                text="📦 DEVOLVER PELÍCULA", 
                                command=self.devolver,
                                style='Devolver.TButton')
        btn_devolver.grid(row=0, column=1, padx=10)
        
        btn_actualizar = ttk.Button(frame_botones, 
                                  text="🔄 ACTUALIZAR CATÁLOGO", 
                                  command=self.actualizar,
                                  style='Actualizar.TButton')
        btn_actualizar.grid(row=0, column=2, padx=10)
        
        # Footer
        footer = tk.Label(main_frame, 
                         text="© 2025 CINEMA PLAY - Todos los derechos reservados", 
                         font=('Verdana', 9),
                         bg='#f4f4f9',
                         fg="#000000")
        footer.pack(side='bottom', pady=(10, 0))
    
    def agregar_datos_ejemplo(self):
        self.peliculas_ejemplo = [
            ("El Padrino", "Drama/Crimen", "🟢 Disponible"),
            ("Pulp Fiction", "Crimen/Drama", "🟢 Disponible"),
            ("El Señor de los Anillos", "Fantasía/Aventura", "🔴 Rentada"),
            ("Matrix", "Ciencia Ficción", "🟢 Disponible"),
            ("Forrest Gump", "Drama/Comedia", "🔴 Rentada"),
            ("Interestelar", "Ciencia Ficción", "🟢 Disponible"),
            ("El Rey León", "Animación/Musical", "🟡 Próximamente"),
            ("Titanic", "Romance/Drama", "🟢 Disponible")
        ]
        
        for pelicula in self.peliculas_ejemplo:
            self.tabla.insert("", "end", values=pelicula)
    
    def buscar_pelicula(self):
        nombre = self.entry_busqueda.get().strip().lower()
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Filtrar películas
        resultados = [p for p in self.peliculas_ejemplo if nombre in p[0].lower()]
        
        if resultados:
            for pelicula in resultados:
                self.tabla.insert("", "end", values=pelicula)
        else:
            messagebox.showinfo("Búsqueda", f"No se encontró la película: {nombre}")
    
    def rentar(self):
        messagebox.showinfo("Acción", "Función de rentar en construcción")
    
    def devolver(self):
        messagebox.showinfo("Acción", "Función de devolver en construcción")
    
    def actualizar(self):
        # Restaurar todas las películas
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for pelicula in self.peliculas_ejemplo:
            self.tabla.insert("", "end", values=pelicula)

if __name__ == "__main__":
    app = CatalogoPeliculasView()
    app.mainloop()