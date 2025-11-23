# VIEWS/menu_principal.py

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import hashlib

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración principal
        self.title("CINEMA PLAY - Sistema de Rentas")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.configure(bg="#000000")

        # Conexión a la base de datos
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;"
            "DATABASE=cineplus;"
            "Trusted_Connection=yes;"
        )

        # Construir interfaz
        self.create_login_interface()

        # Centrar ventana DESPUÉS de crear los widgets
        self.after(100, self.center_window)

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = 1000
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def hash_password(self, password):
        """Hashear la contraseña para comparar con la almacenada"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_login_interface(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#000000")
        main_frame.pack(fill="both", expand=True)

        # Header con logo
        header_frame = tk.Frame(main_frame, bg="#000000", height=80)
        header_frame.pack(fill="x", padx=50, pady=20)
        header_frame.pack_propagate(False)

        logo_label = tk.Label(
            header_frame,
            text="CINEMA PLAY",
            font=("Arial", 32, "bold"),
            bg="#000000",
            fg="#E50914"
        )
        logo_label.pack(side="left")

        # Frame central con contenido principal
        center_frame = tk.Frame(main_frame, bg="#000000")
        center_frame.pack(fill="both", expand=True, pady=50)

        # Título principal
        title_label = tk.Label(
            center_frame,
            text="Películas ilimitadas y mucho más",
            font=("Arial", 28, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        title_label.pack(pady=(0, 20))

        # Subtítulo
        subtitle_label = tk.Label(
            center_frame,
            text="Disfruta donde quieras. Cancela cuando quieras.",
            font=("Arial", 16),
            bg="#000000",
            fg="#FFFFFF"
        )
        subtitle_label.pack(pady=(0, 40))

        # Texto descriptivo
        desc_label = tk.Label(
            center_frame,
            text="¿Quieres ver CINEMA PLAY ya? Ingresa tus credenciales.",
            font=("Arial", 14),
            bg="#000000",
            fg="#FFFFFF"
        )
        desc_label.pack(pady=(0, 30))

        # Frame de formulario de login
        login_frame = tk.Frame(center_frame, bg="#000000")
        login_frame.pack(pady=20)

        # Etiqueta de email
        email_label = tk.Label(
            login_frame,
            text="Email",
            font=("Arial", 12, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        email_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 5))

        # Campo de entrada de email
        self.email_entry = tk.Entry(
            login_frame,
            width=40,
            font=("Arial", 14),
            bg="#333333",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat"
        )
        self.email_entry.grid(row=1, column=0, padx=(0, 10), pady=(0, 15))

        # Etiqueta de contraseña
        password_label = tk.Label(
            login_frame,
            text="Contraseña",
            font=("Arial", 12, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        password_label.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 5))

        # Campo de entrada de contraseña
        self.password_entry = tk.Entry(
            login_frame,
            width=40,
            font=("Arial", 14),
            bg="#333333",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            show="*"
        )
        self.password_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 15))

        # Botón de comenzar
        self.start_button = tk.Button(
            login_frame,
            text="Comenzar →",
            font=("Arial", 14, "bold"),
            bg="#E50914",
            fg="#FFFFFF",
            activebackground="#B2070F",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.verificar_usuario,
            padx=30,
            pady=10
        )
        self.start_button.grid(row=2, column=0, columnspan=2, pady=(20, 0))

        # Enlace para presionar Enter
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.verificar_usuario())

        # Footer
        footer_frame = tk.Frame(main_frame, bg="#000000", height=50)
        footer_frame.pack(fill="x", side="bottom", pady=20)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="© 2025 CINEMA PLAY - Todos los derechos reservados",
            font=("Arial", 10),
            bg="#000000",
            fg="#666666"
        )
        footer_label.pack()

        # Hacer focus en el campo de email al iniciar
        self.email_entry.focus()

    def verificar_usuario(self):
        """Verificar el email y contraseña en la base de datos y redirigir según el rol"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Advertencia", "Por favor ingresa tanto el email como la contraseña.")
            return

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Buscar el email en DatosIdentificacion y verificar contraseña
            cursor.execute("""
                SELECT di.id_datos, di.nombre, di.apellido, di.contraseña 
                FROM DatosIdentificacion di 
                WHERE di.correo = ?
            """, email)

            datos_usuario = cursor.fetchone()

            if not datos_usuario:
                messagebox.showerror(
                    "Error de autenticación", 
                    "Email o contraseña incorrectos."
                )
                conn.close()
                return

            id_datos = datos_usuario[0]
            nombre = datos_usuario[1]
            apellido = datos_usuario[2]
            contraseña_almacenada = datos_usuario[3]

            # Verificar contraseña (comparar hash)
            password_hash = self.hash_password(password)
            if password_hash != contraseña_almacenada:
                # También verificar si la contraseña está en texto plano (para compatibilidad)
                if password != contraseña_almacenada:
                    messagebox.showerror(
                        "Error de autenticación", 
                        "Email o contraseña incorrectos."
                    )
                    conn.close()
                    return

            # Verificar si es empleado
            cursor.execute("SELECT id_empleado FROM Empleado WHERE id_datos = ?", id_datos)
            empleado = cursor.fetchone()

            # Verificar si es cliente
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_datos = ?", id_datos)
            cliente = cursor.fetchone()

            conn.close()

            # Redirigir según el rol
            if empleado:
                self.abrir_panel_empleado(nombre, apellido, id_datos)
            elif cliente:
                self.abrir_panel_cliente(nombre, apellido, id_datos)
            else:
                messagebox.showwarning(
                    "Rol no definido", 
                    "Tu cuenta no tiene un rol asignado. Contacta al administrador."
                )

        except pyodbc.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo verificar el usuario: {e}")

    def abrir_panel_empleado(self, nombre, apellido, id_datos):
        """Abrir panel de administrador/empleado"""
        try:
            # Importación diferida para evitar problemas circulares
            from empleado_view import EmpleadoView
            
            self.withdraw()  # Ocultar ventana principal
            
            # Crear ventana de empleado
            empleado_window = tk.Toplevel(self)
            app_empleado = EmpleadoView(empleado_window, f"{nombre} {apellido}")
            
            # Configurar comportamiento al cerrar
            empleado_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana_secundaria(empleado_window))
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se encontró el módulo empleado_view: {e}")
            self.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el panel de empleado: {e}")
            self.deiconify()

    def abrir_panel_cliente(self, nombre, apellido, id_datos):
        """Abrir panel de cliente"""
        try:
            # Importación diferida para evitar problemas circulares
            from cliente_view import CatalogoPeliculasView
            
            # Obtener el id_cliente
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_datos = ?", id_datos)
            cliente_data = cursor.fetchone()
            conn.close()
            
            id_cliente = cliente_data[0] if cliente_data else None
            
            self.withdraw()  # Ocultar ventana principal
            
            # Crear ventana de cliente
            cliente_window = tk.Toplevel(self)
            app_cliente = CatalogoPeliculasView(cliente_window, f"{nombre} {apellido}", id_cliente)
            
            # Configurar comportamiento al cerrar
            cliente_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana_secundaria(cliente_window))
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se encontró el módulo cliente_view: {e}")
            self.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el catálogo de usuario: {e}")
            self.deiconify()

    def cerrar_ventana_secundaria(self, ventana):
        """Manejar el cierre de ventanas secundarias"""
        ventana.destroy()
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        """Mostrar ventana principal cuando se cierren las otras"""
        self.deiconify()
        # Limpiar campos al volver
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.focus()

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()

    