import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

class PeliculaView(tk.Toplevel):
    def __init__(self, parent, modo="agregar", datos_pelicula=None):
        super().__init__(parent)
        self.parent = parent
        self.modo = modo  # "agregar" o "editar"
        self.datos_pelicula = datos_pelicula
        self.pelicula_id = datos_pelicula[0] if datos_pelicula else None
        
        self.title("🎬 Gestión de Películas - CINEMA PLAY")
        self.geometry("900x600")
        self.configure(bg="#F2F6FF")
        self.transient(parent)
        self.grab_set()

        # Conexión a la base de datos
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;"
            "DATABASE=cineplus;"
            "Trusted_Connection=yes;"
        )
        self.conn = self.conectar_db()

        self.crear_interfaz()
        if self.modo == "editar":
            self.cargar_datos_edicion()

    def conectar_db(self):
        """Conectar a la base de datos"""
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def crear_interfaz(self):
        # ========== HEADER ==========
        header = tk.Frame(self, bg="#1F6FEB", height=60)
        header.pack(fill="x")

        titulo = "Editar Película" if self.modo == "editar" else "Registrar Nueva Película"
        tk.Label(
            header,
            text=f"🎬 {titulo}",
            bg="#1F6FEB",
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # ========== CARD FORMULARIO ==========
        card = tk.Frame(self, bg="white", bd=2, relief="groove", padx=20, pady=20)
        card.pack(pady=15, padx=25, fill="x")

        tk.Label(
            card,
            text="Información de la Película",
            bg="white",
            fg="#0D2B60",
            font=("Segoe UI", 15, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="w")

        # ---------- TÍTULO ----------
        tk.Label(
            card, text="Título:*", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=0, sticky="w", padx=5, pady=8)

        self.titulo_entry = tk.Entry(
            card, width=35, font=("Segoe UI", 11),
            relief="solid", bd=1, bg="#F8F9FA"
        )
        self.titulo_entry.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        # ---------- GÉNERO ----------
        tk.Label(
            card, text="Género:*", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=1, column=2, sticky="w", padx=5, pady=8)

        self.genero_combo = ttk.Combobox(
            card,
            values=[
                "Acción", "Aventura", "Comedia", "Drama", "Romance",
                "Terror", "Ciencia Ficción", "Suspenso", "Animación",
                "Documental", "Fantasía", "Crimen", "Musical", "Biografía"
            ],
            width=20,
            font=("Segoe UI", 11),
            state="readonly"
        )
        self.genero_combo.grid(row=1, column=3, padx=5, pady=8, sticky="w")

        # ---------- DURACIÓN ----------
        tk.Label(
            card, text="Duración (min):*", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=2, column=0, sticky="w", padx=5, pady=8)

        self.duracion_entry = tk.Entry(
            card, width=15, font=("Segoe UI", 11),
            relief="solid", bd=1, bg="#F8F9FA"
        )
        self.duracion_entry.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        # ---------- PRECIO RENTA ----------
        tk.Label(
            card, text="Precio Renta ($):*", bg="white", fg="#0D2B60",
            font=("Segoe UI", 11, "bold")
        ).grid(row=2, column=2, sticky="w", padx=5, pady=8)

        self.precio_entry = tk.Entry(
            card, width=15, font=("Segoe UI", 11),
            relief="solid", bd=1, bg="#F8F9FA"
        )
        self.precio_entry.grid(row=2, column=3, padx=5, pady=8, sticky="w")

        # ========== BOTONES ==========
        frame_btn = tk.Frame(self, bg="#F2F6FF")
        frame_btn.pack(pady=15)

        if self.modo == "agregar":
            tk.Button(
                frame_btn, text="💾 Guardar Película", bg="#008856", fg="white",
                font=("Segoe UI", 12, "bold"), relief="flat", padx=25, pady=10,
                activebackground="#008F5B", cursor="hand2",
                command=self.guardar_pelicula
            ).pack(side="left", padx=10)
        else:
            tk.Button(
                frame_btn, text="💾 Actualizar Película", bg="#1F6FEB", fg="white",
                font=("Segoe UI", 12, "bold"), relief="flat", padx=25, pady=10,
                activebackground="#1A5FC9", cursor="hand2",
                command=self.actualizar_pelicula
            ).pack(side="left", padx=10)

        tk.Button(
            frame_btn, text="❌ Cancelar", bg="#6C757D", fg="white",
            font=("Segoe UI", 12, "bold"), relief="flat", padx=25, pady=10,
            activebackground="#5A6268", cursor="hand2",
            command=self.destroy
        ).pack(side="left", padx=10)

        # ========== TABLA DE PELÍCULAS EXISTENTES ==========
        tabla_frame = tk.Frame(self, bg="#F2F6FF")
        tabla_frame.pack(fill="both", expand=True, padx=25, pady=10)

        tk.Label(
            tabla_frame,
            text="Catálogo Actual de Películas",
            bg="#F2F6FF",
            fg="#0D2B60",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        columnas = ("ID", "Título", "Género", "Duración", "Precio")
        self.tabla = ttk.Treeview(
            tabla_frame, columns=columnas,
            show="headings", height=8
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading",
                        background="#004AB9",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=25,
                        background="white",
                        fieldbackground="white")

        for col in columnas:
            self.tabla.heading(col, text=col)
            if col == "ID":
                self.tabla.column(col, width=60, anchor="center")
            elif col == "Título":
                self.tabla.column(col, width=250, anchor="w")
            elif col == "Duración":
                self.tabla.column(col, width=80, anchor="center")
            elif col == "Precio":
                self.tabla.column(col, width=80, anchor="center")
            else:
                self.tabla.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_peliculas()

    def cargar_datos_edicion(self):
        """Cargar datos de la película para editar"""
        if self.datos_pelicula:
            # ✅ Asegurarse de que tenemos una lista/tupla con al menos 5 elementos
            if isinstance(self.datos_pelicula, (list, tuple)) and len(self.datos_pelicula) >= 5:
                # Limpiar campos primero
                self.titulo_entry.delete(0, tk.END)
                self.duracion_entry.delete(0, tk.END)
                self.precio_entry.delete(0, tk.END)
                
                # ✅ Insertar datos individuales
                self.titulo_entry.insert(0, str(self.datos_pelicula[1]))  # nombre
                self.genero_combo.set(str(self.datos_pelicula[2]))        # genero
                self.duracion_entry.insert(0, str(self.datos_pelicula[3]))  # duracion
                self.precio_entry.insert(0, str(self.datos_pelicula[4]))    # costo_renta
            else:
                messagebox.showerror("Error", "Datos de película incompletos para edición")

    def cargar_peliculas(self):
        """Cargar todas las películas en la tabla"""
        if not self.conn:
            return

        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            cursor = self.conn.cursor()
            cursor.execute("SELECT id_pelicula, nombre, genero, duracion, costo_renta FROM Pelicula ORDER BY nombre")
            peliculas = cursor.fetchall()

            for pelicula in peliculas:
                # ✅ DESEMPAQUETAR la tupla en variables individuales
                id_pelicula, nombre, genero, duracion, precio = pelicula
                
                # ✅ Insertar los valores individuales, no la tupla completa
                self.tabla.insert("", "end", values=(
                    id_pelicula,      # ID como número
                    nombre,           # Título como string
                    genero,           # Género como string
                    f"{duracion} min", # Duración formateada
                    f"${precio}"      # Precio formateado
                ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las películas: {e}")

    def validar_campos(self):
        """Validar que todos los campos estén completos"""
        titulo = self.titulo_entry.get().strip()
        genero = self.genero_combo.get().strip()
        duracion = self.duracion_entry.get().strip()
        precio = self.precio_entry.get().strip()

        if not titulo:
            messagebox.showwarning("Validación", "El título es obligatorio.")
            self.titulo_entry.focus()
            return False

        if not genero:
            messagebox.showwarning("Validación", "El género es obligatorio.")
            self.genero_combo.focus()
            return False

        if not duracion or not duracion.isdigit():
            messagebox.showwarning("Validación", "La duración debe ser un número válido.")
            self.duracion_entry.focus()
            return False

        if not precio:
            messagebox.showwarning("Validación", "El precio de renta es obligatorio.")
            self.precio_entry.focus()
            return False

        try:
            float(precio)
        except ValueError:
            messagebox.showwarning("Validación", "El precio debe ser un número válido.")
            self.precio_entry.focus()
            return False

        return True

    def guardar_pelicula(self):
        """Guardar nueva película en la base de datos"""
        if not self.validar_campos():
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            titulo = self.titulo_entry.get().strip()
            genero = self.genero_combo.get().strip()
            duracion = float(self.duracion_entry.get().strip())
            precio = float(self.precio_entry.get().strip())

            cursor = self.conn.cursor()
            
            # Verificar si ya existe una película con el mismo nombre
            cursor.execute("SELECT COUNT(*) FROM Pelicula WHERE nombre = ?", titulo)
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Duplicado", f"Ya existe una película con el título: {titulo}")
                return

            # Insertar nueva película
            cursor.execute("""
                INSERT INTO Pelicula (nombre, genero, duracion, costo_renta)
                VALUES (?, ?, ?, ?)
            """, titulo, genero, duracion, precio)

            self.conn.commit()

            messagebox.showinfo("Éxito", f"Película '{titulo}' agregada correctamente.")
            
            # ✅ ACTUALIZAR INMEDIATAMENTE la tabla
            self.cargar_peliculas()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la película: {e}")

    def actualizar_pelicula(self):
        """Actualizar película existente en la base de datos"""
        if not self.validar_campos():
            return

        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            titulo = self.titulo_entry.get().strip()
            genero = self.genero_combo.get().strip()
            duracion = float(self.duracion_entry.get().strip())
            precio = float(self.precio_entry.get().strip())

            cursor = self.conn.cursor()
            
            # Verificar si ya existe otra película con el mismo nombre (excluyendo la actual)
            cursor.execute("SELECT COUNT(*) FROM Pelicula WHERE nombre = ? AND id_pelicula != ?", 
                        titulo, self.pelicula_id)
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Duplicado", f"Ya existe otra película con el título: {titulo}")
                return

            # Actualizar película
            cursor.execute("""
                UPDATE Pelicula 
                SET nombre = ?, genero = ?, duracion = ?, costo_renta = ?
                WHERE id_pelicula = ?
            """, titulo, genero, duracion, precio, self.pelicula_id)

            self.conn.commit()

            messagebox.showinfo("Éxito", f"Película '{titulo}' actualizada correctamente.")
            
            # ✅ ACTUALIZAR INMEDIATAMENTE la tabla
            self.cargar_peliculas()
            # No limpiar campos en edición, mantener datos actualizados

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la película: {e}")


    def limpiar_campos(self):
        """Limpiar todos los campos del formulario"""
        self.titulo_entry.delete(0, tk.END)
        self.genero_combo.set('')
        self.duracion_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.titulo_entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = PeliculaView(root)
    app.mainloop()

