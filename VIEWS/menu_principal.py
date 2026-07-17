# VIEWS/menu_principal.py

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import hashlib
import sys
import os

# Agregar directorios para importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configuración principal
        self.title("🎬 CINEMA PLAY - Sistema de Rentas de Películas")
        self.geometry("1100x700")
        self.resizable(False, False)
        
        # Configurar colores
        self.colors = {
            "primary": "#E50914",     # Rojo Netflix
            "secondary": "#221F1F",   # Negro oscuro
            "accent": "#F5F5F1",      # Blanco roto
            "dark_bg": "#000000",     # Fondo negro
            "card_bg": "#141414",     # Fondo de tarjetas
            "input_bg": "#333333",    # Fondo de inputs
            "text_light": "#FFFFFF",
            "text_muted": "#808080",
            "success": "#46D369",     # Verde
            "hover": "#B81D24",       # Rojo hover
        }
        
        self.configure(bg=self.colors["dark_bg"])

        # Conexión a la base de datos
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;"
            "DATABASE=cineplus;"
            "Trusted_Connection=yes;"
        )

        # Construir interfaz
        self.create_login_interface()

        # Centrar ventana
        self.center_window()
        
        # Configurar navegación con Tab
        self.setup_tab_navigation()

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = 1100
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_tab_navigation(self):
        """Configurar navegación con tecla Tab"""
        # Orden de tabulación
        self.tab_order = [self.email_entry, self.password_entry, self.login_button, self.register_button]
        
        # Configurar comportamiento de Tab
        for widget in self.tab_order:
            if isinstance(widget, tk.Entry):
                widget.bind('<Tab>', self.focus_next_widget)
                widget.bind('<Shift-Tab>', self.focus_previous_widget)
    
    def focus_next_widget(self, event):
        """Mover al siguiente widget con Tab"""
        current = self.focus_get()
        try:
            idx = self.tab_order.index(current)
            next_idx = (idx + 1) % len(self.tab_order)
            self.tab_order[next_idx].focus_set()
        except ValueError:
            pass
        return 'break'
    
    def focus_previous_widget(self, event):
        """Mover al widget anterior con Shift+Tab"""
        current = self.focus_get()
        try:
            idx = self.tab_order.index(current)
            next_idx = (idx - 1) % len(self.tab_order)
            self.tab_order[next_idx].focus_set()
        except ValueError:
            pass
        return 'break'

    def hash_password(self, password):
        """Hashear la contraseña para comparar con la almacenada"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_login_interface(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.colors["dark_bg"])
        main_frame.pack(fill="both", expand=True)

        # Header con logo
        header_frame = tk.Frame(main_frame, bg=self.colors["dark_bg"], height=100)
        header_frame.pack(fill="x", padx=50, pady=20)
        header_frame.pack_propagate(False)

        logo_label = tk.Label(
            header_frame,
            text="🎬 CINEMA PLAY",
            font=("Arial", 36, "bold"),
            bg=self.colors["dark_bg"],
            fg=self.colors["primary"]
        )
        logo_label.pack(side="left")

        subtitle_label = tk.Label(
            header_frame,
            text="Sistema de Rentas",
            font=("Arial", 14),
            bg=self.colors["dark_bg"],
            fg=self.colors["accent"]
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=15)

        # Frame central con contenido
        center_frame = tk.Frame(main_frame, bg=self.colors["dark_bg"])
        center_frame.pack(fill="both", expand=True, padx=100, pady=20)

        # Lado izquierdo - Texto promocional
        left_frame = tk.Frame(center_frame, bg=self.colors["dark_bg"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 50))

        title_label = tk.Label(
            left_frame,
            text="Bienvenido al\nMejor Cine\nEn Línea",
            font=("Arial", 32, "bold"),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_light"],
            justify="left"
        )
        title_label.pack(anchor="w", pady=(0, 30))

        # Beneficios
        benefits_frame = tk.Frame(left_frame, bg=self.colors["dark_bg"])
        benefits_frame.pack(anchor="w", pady=(0, 30))

        benefits = [
            "✅ Catálogo con miles de películas",
            "✅ Estrenos exclusivos cada semana",
            "✅ Sin anuncios, experiencia premium",
            "✅ Soporte 24/7 disponible",
            "✅ Compatible con todos tus dispositivos"
        ]

        for benefit in benefits:
            tk.Label(
                benefits_frame,
                text=benefit,
                font=("Arial", 12),
                bg=self.colors["dark_bg"],
                fg=self.colors["accent"],
                anchor="w"
            ).pack(anchor="w", pady=2)

        # Lado derecho - Formulario de login
        right_frame = tk.Frame(center_frame, bg=self.colors["card_bg"], 
                              relief="flat", bd=0)
        right_frame.pack(side="right", fill="both", expand=False, 
                        padx=20, pady=20, ipadx=40, ipady=30)

        # Título del formulario
        form_title = tk.Label(
            right_frame,
            text="Iniciar Sesión",
            font=("Arial", 24, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_light"]
        )
        form_title.pack(pady=(0, 30))

        # Campo Email
        email_container = tk.Frame(right_frame, bg=self.colors["card_bg"])
        email_container.pack(fill="x", pady=(0, 20))

        email_label = tk.Label(
            email_container,
            text="Email",
            font=("Arial", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_light"]
        )
        email_label.pack(anchor="w")

        self.email_entry = tk.Entry(
            email_container,
            width=35,
            font=("Arial", 12),
            bg=self.colors["input_bg"],
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            bd=2
        )
        self.email_entry.pack(fill="x", pady=(5, 0), ipady=8)
        self.email_entry.config(highlightbackground=self.colors["text_muted"], 
                              highlightcolor=self.colors["primary"], 
                              highlightthickness=1)

        # Campo Contraseña
        password_container = tk.Frame(right_frame, bg=self.colors["card_bg"])
        password_container.pack(fill="x", pady=(0, 20))

        password_label = tk.Label(
            password_container,
            text="Contraseña",
            font=("Arial", 11, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text_light"]
        )
        password_label.pack(anchor="w")

        # Frame para contraseña con botón de visibilidad
        password_frame = tk.Frame(password_container, bg=self.colors["input_bg"])
        password_frame.pack(fill="x", pady=(5, 0))

        self.password_entry = tk.Entry(
            password_frame,
            width=30,
            font=("Arial", 12),
            bg=self.colors["input_bg"],
            fg=self.colors["text_light"],
            insertbackground=self.colors["text_light"],
            relief="flat",
            bd=0,
            show="•"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, 
                               ipady=8, padx=(2, 0))

        # Botón para mostrar/ocultar contraseña
        self.show_password_var = tk.BooleanVar(value=False)
        self.show_password_btn = tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 10),
            bg=self.colors["input_bg"],
            fg=self.colors["text_muted"],
            activebackground=self.colors["input_bg"],
            activeforeground=self.colors["primary"],
            relief="flat",
            cursor="hand2",
            command=self.toggle_password_visibility
        )
        self.show_password_btn.pack(side="right", padx=5)
        
        # Configurar borde del frame de contraseña
        password_frame.config(highlightbackground=self.colors["text_muted"], 
                            highlightcolor=self.colors["primary"], 
                            highlightthickness=1)

        # Botón de Iniciar Sesión
        self.login_button = tk.Button(
            right_frame,
            text="🎬 INGRESAR",
            font=("Arial", 14, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["text_light"],
            activebackground=self.colors["hover"],
            activeforeground=self.colors["text_light"],
            relief="flat",
            cursor="hand2",
            command=self.verificar_usuario,
            padx=30,
            pady=12,
            bd=0
        )
        self.login_button.pack(pady=(20, 15), fill="x")
        
        # Efecto hover para el botón
        self.login_button.bind("<Enter>", 
                             lambda e: self.login_button.config(bg=self.colors["hover"]))
        self.login_button.bind("<Leave>", 
                             lambda e: self.login_button.config(bg=self.colors["primary"]))

        # Botón de registro
        self.register_button = tk.Button(
            right_frame,
            text="📝 Crear Cuenta Nueva",
            font=("Arial", 11),
            bg=self.colors["card_bg"],
            fg=self.colors["accent"],
            activebackground=self.colors["card_bg"],
            activeforeground=self.colors["primary"],
            relief="flat",
            cursor="hand2",
            command=self.abrir_registro,
            padx=20,
            pady=8,
            bd=1,
            highlightbackground=self.colors["accent"]
        )
        self.register_button.pack(pady=(10, 5))

        # Enlace para presionar Enter
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.verificar_usuario())

        # Footer
        footer_frame = tk.Frame(main_frame, bg=self.colors["dark_bg"], height=50)
        footer_frame.pack(fill="x", side="bottom", pady=20)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="© 2025 CINEMA PLAY - Todos los derechos reservados | Contacto: soporte@cinemaplay.com",
            font=("Arial", 10),
            bg=self.colors["dark_bg"],
            fg=self.colors["text_muted"]
        )
        footer_label.pack()

        # Hacer focus en el campo de email al iniciar
        self.email_entry.focus()

    def toggle_password_visibility(self):
        """Alternar entre mostrar y ocultar la contraseña"""
        if self.password_entry.cget('show') == '•':
            self.password_entry.config(show='')
            self.show_password_btn.config(text="🔒")
        else:
            self.password_entry.config(show='•')
            self.show_password_btn.config(text="👁")

    def verificar_usuario(self):
        """Verificar el email y contraseña en la base de datos y redirigir según el rol"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Acceso Requerido", 
                                 "Por favor ingresa tanto el email como la contraseña.")
            return

        try:
            # Animación de carga en el botón
            original_text = self.login_button.cget("text")
            self.login_button.config(text="VERIFICANDO...", state="disabled")
            self.update()

            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Buscar el email en DatosIdentificacion
            cursor.execute("""
                SELECT di.id_datos, di.nombre, di.apellido, di.contraseña 
                FROM DatosIdentificacion di 
                WHERE di.correo = ?
            """, email)

            datos_usuario = cursor.fetchone()

            if not datos_usuario:
                messagebox.showerror(
                    "Acceso Denegado", 
                    "Email o contraseña incorrectos."
                )
                self.login_button.config(text=original_text, state="normal")
                conn.close()
                return

            id_datos = datos_usuario[0]
            nombre = datos_usuario[1]
            apellido = datos_usuario[2]
            contraseña_almacenada = datos_usuario[3]

            # Verificar contraseña
            password_hash = self.hash_password(password)
            if password_hash != contraseña_almacenada:
                if password != contraseña_almacenada:
                    messagebox.showerror(
                        "Acceso Denegado", 
                        "Email o contraseña incorrectos."
                    )
                    self.login_button.config(text=original_text, state="normal")
                    conn.close()
                    return

            # Verificar si es empleado
            cursor.execute("SELECT id_empleado FROM Empleado WHERE id_datos = ?", id_datos)
            empleado = cursor.fetchone()

            # Verificar si es cliente
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_datos = ?", id_datos)
            cliente = cursor.fetchone()

            conn.close()

            # Restaurar botón
            self.login_button.config(text="ACCESO CONCEDIDO", state="normal")
            self.update()
            self.after(500, lambda: self.login_button.config(text=original_text, state="normal"))

            # Redirigir según el rol
            if empleado:
                self.after(800, lambda: self.abrir_panel_empleado(nombre, apellido, id_datos))
            elif cliente:
                self.after(800, lambda: self.abrir_panel_cliente(nombre, apellido, id_datos))
            else:
                messagebox.showwarning(
                    "Rol no definido", 
                    "Tu cuenta no tiene un rol asignado. Contacta al administrador."
                )
                self.login_button.config(text=original_text, state="normal")

        except pyodbc.Error as e:
            messagebox.showerror("Error de Base de Datos", 
                               f"No se pudo conectar a la base de datos:\n{e}")
            self.login_button.config(text=original_text, state="normal")
        except Exception as e:
            messagebox.showerror("Error", 
                               f"No se pudo verificar el usuario:\n{e}")
            self.login_button.config(text=original_text, state="normal")

    def abrir_panel_empleado(self, nombre, apellido, id_datos):
        """Abrir panel de administrador/empleado"""
        try:
            from VIEWS.empleado_view import EmpleadoView
            
            self.withdraw()  # Ocultar ventana principal
            
            empleado_window = tk.Toplevel(self)
            app_empleado = EmpleadoView(empleado_window, f"{nombre} {apellido}")
            
            empleado_window.protocol("WM_DELETE_WINDOW", 
                                   lambda: self.cerrar_ventana_secundaria(empleado_window))
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se encontró el módulo empleado_view:\n{e}")
            self.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el panel de empleado:\n{e}")
            self.deiconify()

    def abrir_panel_cliente(self, nombre, apellido, id_datos):
        """Abrir panel de cliente - CATÁLOGO de películas"""
        try:
            # Obtener el id_cliente
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("SELECT id_cliente FROM Cliente WHERE id_datos = ?", id_datos)
            cliente_data = cursor.fetchone()
            conn.close()
            
            id_cliente = cliente_data[0] if cliente_data else None
            
            from VIEWS.cliente_view import CatalogoPeliculasView
            
            self.withdraw()  # Ocultar ventana principal
            
            cliente_window = tk.Toplevel(self)
            app_cliente = CatalogoPeliculasView(cliente_window, f"{nombre} {apellido}", id_cliente)
            
            cliente_window.protocol("WM_DELETE_WINDOW", 
                                  lambda: self.cerrar_ventana_secundaria(cliente_window))
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se encontró el módulo cliente_view:\n{e}")
            self.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el catálogo de usuario:\n{e}")
            self.deiconify()

    def cerrar_ventana_secundaria(self, ventana):
        """Manejar el cierre de ventanas secundarias"""
        ventana.destroy()
        self.mostrar_menu_principal()
        
    def abrir_registro(self):
        """Abrir ventana de registro"""
        try:
            from VIEWS.registro_view import RegistroView
            registro_window = RegistroView(self)
            registro_window.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro:\n{e}")

    def mostrar_menu_principal(self):
        """Mostrar ventana principal cuando se cierren las otras"""
        self.deiconify()
        # Limpiar campos al volver
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.focus()