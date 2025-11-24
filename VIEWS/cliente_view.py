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
        
         # Botón "Mis Rentas" - NUEVO
        btn_mis_rentas = ttk.Button(frame_botones, 
                                  text="📋 Mis Rentas Activas", 
                                  command=self.ver_mis_rentas,
                                  style='Actualizar.TButton')
        btn_mis_rentas.grid(row=0, column=0, padx=10)
        
        # Frame de botones de acción SECUNDARIO (los botones originales)
        frame_botones = tk.Frame(main_frame, bg='#f4f4f9')
        frame_botones.pack(pady=5)
        
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
                        WHEN EXISTS (
                            SELECT 1 FROM Renta r 
                            WHERE r.id_pelicula = p.id_pelicula 
                            AND r.estado = 'Activa'
                        ) 
                        THEN 'Rentada :(' 
                        ELSE 'Disponible :D' 
                    END as estado
                FROM Pelicula p
                ORDER BY p.nombre
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


    def ver_mis_rentas(self):
        """Ver las rentas activas del usuario"""
        try:
            if not self.conn:
                messagebox.showerror("Error", "No hay conexión a la base de datos")
                return
                
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    r.id_renta,
                    p.nombre as pelicula,
                    r.fecha_inicio,
                    r.fecha_devolucion,
                    DATEDIFF(day, GETDATE(), r.fecha_devolucion) as dias_restantes
                FROM Renta r
                JOIN Pelicula p ON r.id_pelicula = p.id_pelicula
                WHERE r.id_cliente = ? AND r.estado = 'Activa'
                ORDER BY r.fecha_devolucion
            """, self.id_cliente)
            
            rentas = cursor.fetchall()
            
            if not rentas:
                messagebox.showinfo("Mis Rentas", "No tienes películas rentadas actualmente.")
                return
            
            # Crear ventana para mostrar rentas
            ventana_rentas = tk.Toplevel(self)
            ventana_rentas.title("📋 Mis Rentas Activas")
            ventana_rentas.geometry("700x400")
            ventana_rentas.configure(bg='#f4f4f9')
            
            tk.Label(
                ventana_rentas,
                text="🎬 Mis Rentas Activas",
                font=('Verdana', 14, 'bold'),
                bg='#f4f4f9',
                fg="#000000"
            ).pack(pady=10)
            
            # Tabla de rentas
            frame_tabla = tk.Frame(ventana_rentas, bg="#f4f4f9")
            frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
            
            columnas = ("ID", "Película", "Fecha Inicio", "Fecha Devolución", "Días Restantes")
            tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
            
            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=120, anchor='center')
            
            # Insertar datos
            for renta in rentas:
                id_renta, pelicula, fecha_inicio, fecha_devolucion, dias_restantes = renta
                
                # ✅ CORREGIDO: Manejar fechas como strings o datetime
                try:
                    # Si es datetime, formatear
                    if hasattr(fecha_inicio, 'strftime'):
                        fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y")
                    else:
                        # Si ya es string, usar directamente o convertir
                        fecha_inicio_str = str(fecha_inicio)
                    
                    if hasattr(fecha_devolucion, 'strftime'):
                        fecha_devolucion_str = fecha_devolucion.strftime("%d/%m/%Y")
                    else:
                        fecha_devolucion_str = str(fecha_devolucion)
                        
                except Exception as e:
                    # En caso de error, mostrar valores originales
                    fecha_inicio_str = str(fecha_inicio) if fecha_inicio else "N/A"
                    fecha_devolucion_str = str(fecha_devolucion) if fecha_devolucion else "N/A"
                
                dias_texto = f"{dias_restantes} días" if dias_restantes >= 0 else f"Vencida ({abs(dias_restantes)} días)"
                
                tabla.insert("", "end", values=(
                    id_renta,
                    pelicula,
                    fecha_inicio_str,
                    fecha_devolucion_str,
                    dias_texto
                ))
            
            scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
            tabla.configure(yscrollcommand=scrollbar.set)
            
            tabla.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las rentas:\n{e}")

    def rentar_pelicula(self):
        """Rentar película seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona una película para rentar.")
            return

        try:
            item = self.tabla.item(seleccion[0])
            valores = item['values']
            id_pelicula = int(valores[0])  # ✅ Asegurar que sea INT
            titulo_pelicula = valores[1]
            
            precio_str = valores[4].replace('$', '').strip()
            precio = float(precio_str)

            # Verificar disponibilidad
            estado = valores[5] if len(valores) > 5 else ""
            if "Rentada" in estado:
                messagebox.showwarning("No Disponible", f"La película '{titulo_pelicula}' ya está rentada.")
                return

            respuesta = messagebox.askyesno(
                "Confirmar Renta",
                f"¿Rentar '{titulo_pelicula}' por ${precio:.2f}?"
            )

            if respuesta:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO Renta (id_cliente, id_pelicula, fecha_inicio, fecha_devolucion, estado)
                    VALUES (?, ?, GETDATE(), DATEADD(day, 7, GETDATE()), 'Activa')
                """, self.id_cliente, id_pelicula)

                self.conn.commit()

                messagebox.showinfo("Éxito", f"✅ '{titulo_pelicula}' rentada correctamente!")
                self.cargar_peliculas()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la renta: {e}")

    def devolver_pelicula(self):
        """Devolver película rentada por el usuario"""
        try:
            if not self.conn:
                messagebox.showerror("Error", "No hay conexión a la base de datos")
                return
                
            # Obtener rentas activas del usuario
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT r.id_renta, p.nombre, r.fecha_inicio, r.fecha_devolucion
                FROM Renta r
                JOIN Pelicula p ON r.id_pelicula = p.id_pelicula
                WHERE r.id_cliente = ? AND r.estado = 'Activa'
                ORDER BY r.fecha_devolucion
            """, self.id_cliente)
            
            rentas_activas = cursor.fetchall()
            
            if not rentas_activas:
                messagebox.showinfo(
                    "Devolución", 
                    "No tienes películas rentadas actualmente."
                )
                return
            
            # Crear ventana de selección
            self.mostrar_ventana_devolucion(rentas_activas)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las rentas activas:\n{e}")

    def mostrar_ventana_devolucion(self, rentas_activas):
        """Mostrar ventana para seleccionar película a devolver"""
        ventana_devolucion = tk.Toplevel(self)
        ventana_devolucion.title("📦 Devolver Película")
        ventana_devolucion.geometry("600x400")
        ventana_devolucion.configure(bg='#f4f4f9')
        ventana_devolucion.transient(self)
        ventana_devolucion.grab_set()
        
        # Título
        tk.Label(
            ventana_devolucion,
            text="🎬 Selecciona la Película a Devolver",
            font=('Verdana', 14, 'bold'),
            bg='#f4f4f9',
            fg="#000000"
        ).pack(pady=10)
        
        # Frame de la tabla
        frame_tabla = tk.Frame(ventana_devolucion, bg="#f4f4f9")
        frame_tabla.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tabla de rentas activas
        columnas = ("ID Renta", "Película", "Fecha Inicio", "Fecha Límite")
        tabla_rentas = ttk.Treeview(
            frame_tabla, 
            columns=columnas, 
            show="headings",
            height=8
        )
        
        # Configurar columnas
        for col in columnas:
            tabla_rentas.heading(col, text=col)
            tabla_rentas.column(col, width=120, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_rentas.yview)
        tabla_rentas.configure(yscrollcommand=scrollbar.set)
        
        # Insertar datos
        for renta in rentas_activas:
            id_renta, pelicula, fecha_inicio, fecha_devolucion = renta
            
            # ✅ CORREGIDO: Manejar fechas correctamente
            try:
                if hasattr(fecha_inicio, 'strftime'):
                    fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y")
                else:
                    fecha_inicio_str = str(fecha_inicio)
                
                if hasattr(fecha_devolucion, 'strftime'):
                    fecha_devolucion_str = fecha_devolucion.strftime("%d/%m/%Y")
                else:
                    fecha_devolucion_str = str(fecha_devolucion)
                    
            except Exception:
                fecha_inicio_str = str(fecha_inicio) if fecha_inicio else "N/A"
                fecha_devolucion_str = str(fecha_devolucion) if fecha_devolucion else "N/A"
            
            tabla_rentas.insert("", "end", values=(
                id_renta,
                pelicula,
                fecha_inicio_str,
                fecha_devolucion_str
            ))
        
        tabla_rentas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame de botones
        frame_botones = tk.Frame(ventana_devolucion, bg='#f4f4f9')
        frame_botones.pack(pady=10)
        
        # Botón devolver
        btn_devolver = ttk.Button(
            frame_botones,
            text="✅ Devolver Película Seleccionada",
            command=lambda: self.procesar_devolucion(tabla_rentas, ventana_devolucion),
            style='Devolver.TButton'
        )
        btn_devolver.pack(side='left', padx=10)
        
        # Botón cancelar
        btn_cancelar = ttk.Button(
            frame_botones,
            text="❌ Cancelar",
            command=ventana_devolucion.destroy
        )
        btn_cancelar.pack(side='left', padx=10)

    def procesar_devolucion(self, tabla_rentas, ventana_devolucion):
        """Procesar la devolución de la película seleccionada"""
        seleccion = tabla_rentas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona una película para devolver.")
            return
        
        item = tabla_rentas.item(seleccion[0])
        valores = item['values']
        id_renta = valores[0]
        nombre_pelicula = valores[1]
        
        # Confirmar devolución
        respuesta = messagebox.askyesno(
            "Confirmar Devolución",
            f"¿Estás seguro de devolver la película:\n\n"
            f"🎬 {nombre_pelicula}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                # Realizar la devolución
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE Renta 
                    SET estado = 'Devuelto', fecha_devolucion = GETDATE()
                    WHERE id_renta = ?
                """, id_renta)
                
                self.conn.commit()
                
                messagebox.showinfo(
                    "Devolución Exitosa",
                    f"✅ Película devuelta correctamente:\n\n"
                    f"🎬 {nombre_pelicula}\n\n"
                    f"¡Gracias por tu preferencia!"
                )
                
                # Cerrar ventana y actualizar
                ventana_devolucion.destroy()
                self.cargar_peliculas()  # Actualizar estado en el catálogo
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la devolución:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoPeliculasView(root, "Cliente Ejemplo")
    app.mainloop()

