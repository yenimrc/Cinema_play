import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime



class EmpleadoView(tk.Toplevel):
    def __init__(self, parent, nombre_empleado=""):
        super().__init__(parent)
        self.title("🎬 Panel del Empleado - Catálogo de Películas")
        self.geometry("900x600")
        self.configure(bg='#f5f5f5')
        self.parent = parent
        self.transient(parent)
        self.grab_set()

        # Conexión a la base de datos
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;"
            "DATABASE=cineplus;"
            "Trusted_Connection=yes;"
        )
        self.conn = None
        self.connect_db()

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
        columnas = ("ID", "Título", "Género", "Duración", "Precio Renta","Estado")
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
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID":
                self.tabla.column(col, width=50)
            elif col == "Título":
                self.tabla.column(col, width=200)
            elif col == "Duración":
                self.tabla.column(col, width=80)
            elif col == "Precio Renta":
                self.tabla.column(col, width=100)
            elif col == "Estado":
                self.tabla.column(col, width=120)
            else:
                self.tabla.column(col, width=150)
        
        self.tabla.pack(pady=10, fill="both", expand=True, padx=20)

        # --- Botones de gestión ---
        frame_botones = tk.Frame(self, bg='#f5f5f5')
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, 
                 text="➕ Agregar", 
                 command=self.agregar_pelicula,
                 bg="#00a616",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=0, padx=8)
        
        tk.Button(frame_botones, 
                 text="✏️ Editar", 
                 command=self.editar_pelicula,
                 bg="#ffc400",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=1, padx=8)
        
        tk.Button(frame_botones, 
                 text="🗑️ Eliminar", 
                 command=self.eliminar_pelicula,
                 bg="#e30404",
                 fg='black',
                 font=('Arial', 10, 'bold'),
                 padx=15,
                 pady=5).grid(row=0, column=2, padx=8)
        
        tk.Button(frame_botones, 
                 text="🔄 Actualizar", 
                 command=self.cargar_peliculas,
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
                text=f"Empleado: {nombre_empleado} | Sesión activa", 
                anchor="w",
                bg='#bbdefb',
                fg='#0d47a1',
                font=('Arial', 10, 'bold')).pack(fill="x", padx=20, pady=8)

        # Cargar datos iniciales
        self.cargar_peliculas()

    def connect_db(self):
        """Conectar a la base de datos"""
        try:
            self.conn = pyodbc.connect(self.connection_string)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            self.destroy()

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
        nombre = self.entry_busqueda.get().strip()
        if not nombre:
            self.cargar_peliculas()
            return
            
        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
            
            cursor = self.conn.cursor()
            # ✅ Incluir el cálculo del estado como en cargar_peliculas
            cursor.execute("""
                SELECT p.id_pelicula, p.nombre, p.genero, p.duracion, p.costo_renta,
                    CASE 
                        WHEN EXISTS (SELECT 1 FROM Renta r WHERE r.id_pelicula = p.id_pelicula AND r.estado = 'Activa') 
                        THEN '🔴 Rentada' 
                        ELSE '🟢 Disponible' 
                    END as estado
                FROM Pelicula p
                WHERE p.nombre LIKE ?
            """, f'%{nombre}%')
            
            peliculas = cursor.fetchall()
            
            if peliculas:
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
            else:
                messagebox.showinfo("Búsqueda", "No se encontraron películas con ese nombre.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")


    def actualizar_lista_peliculas(self):
        """Actualizar la lista de películas en el catálogo"""
        try:
            # Limpiar treeview
            for item in self.tree_peliculas.get_children():
                self.tree_peliculas.delete(item)
            
            # Recargar datos
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_pelicula, nombre, genero, duracion, costo_renta FROM Pelicula ORDER BY nombre")
            peliculas = cursor.fetchall()
            
            for pelicula in peliculas:
                id_pelicula, nombre, genero, duracion, precio = pelicula
                self.tree_peliculas.insert("", "end", values=(
                    id_pelicula, 
                    nombre, 
                    genero, 
                    f"{duracion} min", 
                    f"${precio}"
                ))
                
            print("✅ Lista de películas actualizada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron actualizar las películas: {e}")
            

    def agregar_pelicula(self):
        """Abrir ventana para agregar nueva película"""
        try:
            from pelicula_view import PeliculaView
            ventana = PeliculaView(self, "agregar")
            ventana.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el formulario: {e}")

    def editar_pelicula(self):
        """Editar película seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una película para editar.")
            return
            
        try:
            from pelicula_view import PeliculaView
            item = self.tabla.item(seleccion[0])
            datos = item['values']  # [id, titulo, genero, duracion, precio, estado]
            
            # ✅ Asegurarnos de que solo pasamos los 5 datos necesarios (sin el estado)
            # y que son valores individuales, no tuplas
            if len(datos) >= 5:
                datos_para_editar = datos[:5]  # Toma solo los primeros 5 elementos
                
                # ✅ Verificar que no sean tuplas anidadas
                datos_finales = []
                for dato in datos_para_editar:
                    if isinstance(dato, tuple):
                        # Si es una tupla, tomar el primer elemento
                        datos_finales.append(dato[0] if len(dato) > 0 else "")
                    else:
                        datos_finales.append(dato)
                
                ventana = PeliculaView(self, "editar", datos_finales)
                ventana.grab_set()
            else:
                messagebox.showerror("Error", "No se pudieron obtener los datos completos de la película")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el formulario: {e}")

    def eliminar_pelicula(self):
        """Eliminar película seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una película para eliminar.")
            return
            
        item = self.tabla.item(seleccion[0])
        datos = item['values']
        id_pelicula = datos[0]  # Ahora sí tenemos el ID en la primera posición
        nombre = datos[1]
        
        respuesta = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Está seguro de que desea eliminar la película '{nombre}'?"
        )
        
        if respuesta:
            try:
                cursor = self.conn.cursor()
                
                # Verificar si la película tiene rentas activas
                cursor.execute("SELECT COUNT(*) FROM Renta WHERE id_pelicula = ? AND estado = 'Activa'", id_pelicula)
                rentas_activas = cursor.fetchone()[0]
                
                if rentas_activas > 0:
                    messagebox.showwarning(
                        "No se puede eliminar", 
                        f"No se puede eliminar la película '{nombre}' porque tiene {rentas_activas} renta(s) activa(s)."
                    )
                    return
                
                # Eliminar la película
                cursor.execute("DELETE FROM Pelicula WHERE id_pelicula = ?", id_pelicula)
                self.conn.commit()
                
                messagebox.showinfo("Éxito", f"Película '{nombre}' eliminada correctamente.")
                self.cargar_peliculas()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la película: {e}")

    #se modifico esta parte del codigo ---------------------------
    def ver_rentas(self):
        """Abrir vista de rentas activas"""
        try:
            from renta_view import RentaView
            ventana = RentaView(self, "rentas")
            ventana.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el panel de rentas: {e}")

    #se modifico esta parte del codigo ---------------------------
    def ver_devoluciones(self):
        """Abrir vista de devoluciones"""
        try:
            from renta_view import RentaView
            ventana = RentaView(self, "devoluciones")
            ventana.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el panel de devoluciones: {e}")


    def actualizar_columnas_tabla(self, nuevas_columnas):
        """Actualizar las columnas de la tabla dinámicamente"""
        # Limpiar columnas actuales
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text="")
        
        # Configurar nuevas columnas
        self.tabla["columns"] = nuevas_columnas
        for col in nuevas_columnas:
            self.tabla.heading(col, text=col)
            if col == "ID Renta" or col == "ID Cliente":
                self.tabla.column(col, width=80)
            elif col == "Película":
                self.tabla.column(col, width=200)
            else:
                self.tabla.column(col, width=120)

    def volver_a_peliculas(self):
        """Volver a mostrar el catálogo de películas"""
        columnas = ("ID", "Título", "Género", "Duración", "Precio Renta")
        self.actualizar_columnas_tabla(columnas)
        self.cargar_peliculas()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmpleadoView(root)
    app.mainloop()


