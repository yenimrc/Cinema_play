import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class CatalogoPeliculasView(tk.Toplevel):
    def __init__(self, parent, nombre_cliente="", id_cliente=None):
        super().__init__(parent)
        self.title("🎬 CINEMA PLAY - Catálogo de Películas")
        self.geometry("900x600")
        self.configure(bg='#f4f4f9')
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        self.id_cliente = id_cliente
        
        # Conexión a SQL Server
        self.conn = self.conectar_sql_server()
        
        # Configurar estilo para widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.crear_interfaz(nombre_cliente)
    
    def conectar_sql_server(self):
        """Conectar a la base de datos SQL Server usando Trusted_Connection"""
        try:
            conexion = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=LAPTOP-N1LR75PN;"
                "DATABASE=cineplus;"
                "Trusted_Connection=yes;"
            )
            return conexion
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
            return None
    
    def configure_styles(self):
        """Configurar estilos personalizados para los widgets"""
        self.style.configure('Titulo.TLabel', 
                           background='#f4f4f9', 
                           foreground="#8fa6cb", 
                           font=('Georgia', 20, 'bold'))
        
        # Botones con colores distintos
        self.style.configure('Buscar.TButton',
                           background="#1e5abb",
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Rentar.TButton',
                           background="#0492cf",
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Devolver.TButton',
                           background="#1c66dc",
                           foreground='black',
                           font=('Verdana', 10, 'bold'),
                           padding=(12, 6))
        
        self.style.configure('Actualizar.TButton',
                           background="#afafc5",
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
                           background="#5b76a1",
                           foreground='black',
                           font=('Verdana', 11, 'bold'))
        
        self.style.configure('Entry.TEntry',
                           fieldbackground='#ffffff',
                           foreground='#222222',
                           insertcolor="#0a5ce0")
    
    def crear_interfaz(self, nombre_cliente):
        # Frame principal
        main_frame = tk.Frame(self, bg='#f4f4f9')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Información del cliente
        info_frame = tk.Frame(main_frame, bg='#f4f4f9')
        info_frame.pack(pady=(0, 10), fill='x')
        
        tk.Label(info_frame,
                text=f"👤 Bienvenido: {nombre_cliente}",
                font=('Verdana', 11, 'bold'),
                bg='#f4f4f9',
                fg="#000000").pack()
        
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
                bg="#f4f4f9", 
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
        frame_tabla = tk.Frame(main_frame, bg="#f4f4f9")
        frame_tabla.pack(fill='both', expand=True, pady=(0, 15))
    
        columnas = ("ID","Título", "Género", "Duración", "Precio", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, 
                                columns=columnas, 
                                show="headings", 
                                height=12,
                                style='Custom.Treeview')
        
        # Configurar encabezados
        self.tabla.heading("ID", text="🎯 ID")
        self.tabla.heading("Título", text="🎭 TÍTULO")
        self.tabla.heading("Género", text="🎪 GÉNERO")
        self.tabla.heading("Duración", text="⏱️ DURACIÓN")
        self.tabla.heading("Precio", text="💰 PRECIO")
        self.tabla.heading("Estado", text="📊 ESTADO")
        
        # Configurar anchos de columnas
        self.tabla.column("ID", width=50, anchor='center')
        self.tabla.column("Título", width=300, anchor='center')
        self.tabla.column("Género", width=200, anchor='center')
        self.tabla.column("Duración", width=80, anchor='center')
        self.tabla.column("Precio", width=100, anchor='center')
        self.tabla.column("Estado", width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.cargar_peliculas()
        
        # Frame de botones de acción
        frame_botones = tk.Frame(main_frame, bg='#f4f4f9')
        frame_botones.pack(pady=10)
        
        btn_rentar = ttk.Button(frame_botones, 
                              text="🎟️ RENTAR PELÍCULA", 
                              command=self.rentar_pelicula,
                              style='Rentar.TButton')
        btn_rentar.grid(row=0, column=0, padx=10)
        
        btn_devolver = ttk.Button(frame_botones, 
                                text="📦 DEVOLVER PELÍCULA", 
                                command=self.devolver_pelicula,
                                style='Devolver.TButton')
        btn_devolver.grid(row=0, column=1, padx=10)
        
        btn_actualizar = ttk.Button(frame_botones, 
                                  text="🔄 ACTUALIZAR CATÁLOGO", 
                                  command=self.cargar_peliculas,
                                  style='Actualizar.TButton')
        btn_actualizar.grid(row=0, column=2, padx=10)
        
        # Footer
        footer = tk.Label(main_frame, 
                         text="© 2025 CINEMA PLAY - Todos los derechos reservados", 
                         font=('Verdana', 9),
                         bg='#f4f4f9',
                         fg="#000000")
        footer.pack(side='bottom', pady=(10, 0))
    
    def cargar_peliculas(self):
        """Cargar películas desde SQL Server"""
        try:
            if not self.conn:
                messagebox.showerror("Error", "No hay conexión a la base de datos")
                return
                
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.id_pelicula, p.nombre, p.genero, p.duracion, p.costo_renta,
                    CASE 
                        WHEN EXISTS (SELECT 1 FROM Renta r WHERE r.id_pelicula = p.id_pelicula AND r.estado = 'Activa') 
                        THEN ' Rentada :(' 
                        ELSE ' Disponible :D' 
                    END as estado
                FROM Pelicula p
            """)
            peliculas = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            # Insertar datos
            for pelicula in peliculas:
                id_pelicula, nombre, genero, duracion, precio, estado = pelicula
                self.tabla.insert("", "end", values=(
                    id_pelicula,
                    nombre, 
                    genero,
                    f"{duracion} min", 
                    f"${precio}", 
                    estado
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las películas:\n{e}")

    
    def buscar_pelicula(self):
        """Buscar películas por nombre"""
        nombre = self.entry_busqueda.get().strip().lower()
        if not nombre:
            self.cargar_peliculas()
            return
            
        try:
            if not self.conn:
                messagebox.showerror("Error", "No hay conexión a la base de datos")
                return
                
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT p.id_pelicula, p.nombre, p.genero, p.duracion, p.costo_renta,
                    CASE 
                        WHEN EXISTS (SELECT 1 FROM Renta r WHERE r.id_pelicula = p.id_pelicula AND r.estado = 'Activa') 
                        THEN '🔴 Rentada' 
                        ELSE '🟢 Disponible' 
                    END as estado
                FROM Pelicula p
                WHERE LOWER(p.nombre) LIKE ?
            """, f"%{nombre}%")
            
            resultados = cursor.fetchall()
            
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            if resultados:
                for pelicula in resultados:
                    id_pelicula, nombre, genero, duracion, precio, estado = pelicula
                    self.tabla.insert("", "end", values=(
                        id_pelicula,
                        nombre, 
                        genero,
                        f"{duracion} min", 
                        f"${precio}", 
                        estado
                    ))
            else:
                messagebox.showinfo("Búsqueda", f"No se encontró la película: {nombre}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda:\n{e}")
    
    def rentar_pelicula(self):
        """Rentar la película seleccionada - IMPLEMENTACIÓN COMPLETA"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una película para rentar.")
            return
            
        item = self.tabla.item(seleccion[0])
        datos = item['values']
        id_pelicula = datos[0]
        nombre_pelicula = datos[1]
        precio = datos[4]
        estado = datos[5]
        
        if "Rentada" in estado:
            messagebox.showwarning("No disponible", f"La película '{nombre_pelicula}' ya está rentada.")
            return
        
        # Confirmar renta
        respuesta = messagebox.askyesno(
            "Confirmar Renta",
            f"¿Desea rentar la película?\n\n"
            f"Película: {nombre_pelicula}\n"
            f"Precio: {precio}\n\n"
            f"La renta tendrá una duración de 7 días."
        )
        
        if respuesta:
            try:
                # Usar el id_cliente real del usuario logueado
                if self.id_cliente:
                    id_cliente = self.id_cliente
                else:
                    # Fallback si no hay ID (usar 1 como ejemplo)
                    id_cliente = 1
                    messagebox.showwarning("Advertencia", "Usando cliente de prueba. ID no especificado.")
                
                
                # Calcular fechas
                from datetime import datetime, timedelta
                fecha_inicio = datetime.now().date()
                fecha_devolucion = fecha_inicio + timedelta(days=7)
                
                cursor = self.conn.cursor()
                
                # Insertar renta
                cursor.execute("""
                    INSERT INTO Renta (id_cliente, id_pelicula, fecha_inicio, fecha_devolucion, estado)
                    VALUES (?, ?, ?, ?, 'Activa')
                """, id_cliente, id_pelicula, fecha_inicio, fecha_devolucion)
                
                self.conn.commit()
                
                messagebox.showinfo(
                    "Éxito", 
                    f"✅ Película '{nombre_pelicula}' rentada exitosamente!\n\n"
                    f"📅 Fecha de devolución: {fecha_devolucion.strftime('%d/%m/%Y')}\n"
                    f"💰 Precio: {precio}"
                )
                self.cargar_peliculas()  # Actualizar la vista
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo completar la renta: {e}")
    
    def devolver_pelicula(self):
        """Devolver película rentada"""
        messagebox.showinfo(
        "Devolución", 
        "Para devolver una película, por favor contacte a un empleado.\n\n"
        "Los empleados pueden registrar devoluciones desde el panel de administración."
    )

if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoPeliculasView(root, "Cliente Ejemplo")
    app.mainloop()
