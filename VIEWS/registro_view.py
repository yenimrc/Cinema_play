# VIEWS/registro_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import hashlib
import re

class RegistroView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("🎬 Registro - CINEMA PLAY")
        self.geometry("500x750")
        self.configure(bg="#000000")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Conexión a la base de datos
        self.connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;"
            "DATABASE=cineplus;"
            "Trusted_Connection=yes;"
        )

        self.crear_interfaz()
        self.center_window()

    def center_window(self):
        """Centrar ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def hash_password(self, password):
        """Hashear la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validar_email(self, email):
        """Validar formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#000000")
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)

        # Logo
        logo_label = tk.Label(
            main_frame,
            text="CINEMA PLAY",
            font=("Arial", 24, "bold"),
            bg="#000000",
            fg="#E50914"
        )
        logo_label.pack(pady=(0, 10))

        # Título
        titulo_label = tk.Label(
            main_frame,
            text="Crear Nueva Cuenta",
            font=("Arial", 16, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        titulo_label.pack(pady=(0, 30))

        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg="#000000")
        form_frame.pack(fill="x", pady=10)

        # Campos del formulario
        campos = [
            ("Nombre", "nombre_entry"),
            ("Apellido", "apellido_entry"),
            ("Email", "email_entry"),
            ("Contraseña", "password_entry"),
            ("Confirmar Contraseña", "confirm_password_entry")
        ]

        self.entries = {}
        for i, (texto, key) in enumerate(campos):
            # Etiqueta
            label = tk.Label(
                form_frame,
                text=texto,
                font=("Arial", 11, "bold"),
                bg="#000000",
                fg="#FFFFFF"
            )
            label.grid(row=i*2, column=0, sticky="w", pady=(10, 5))

            # Campo de entrada
            if "contraseña" in texto.lower():
                show_char = "*"
            else:
                show_char = ""

            entry = tk.Entry(
                form_frame,
                width=30,
                font=("Arial", 12),
                bg="#333333",
                fg="#FFFFFF",
                insertbackground="#FFFFFF",
                relief="flat",
                show=show_char
            )
            entry.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 10))
            self.entries[key] = entry

        # Tipo de usuario
        tipo_label = tk.Label(
            form_frame,
            text="Tipo de Usuario",
            font=("Arial", 11, "bold"),
            bg="#000000",
            fg="#FFFFFF"
        )
        tipo_label.grid(row=10, column=0, sticky="w", pady=(10, 5))

        self.tipo_usuario = tk.StringVar(value="cliente")
        
        cliente_radio = tk.Radiobutton(
            form_frame,
            text="Cliente",
            variable=self.tipo_usuario,
            value="cliente",
            bg="#000000",
            fg="#FFFFFF",
            selectcolor="#333333",
            font=("Arial", 10)
        )
        cliente_radio.grid(row=11, column=0, sticky="w", pady=2)

        empleado_radio = tk.Radiobutton(
            form_frame,
            text="Empleado",
            variable=self.tipo_usuario,
            value="empleado",
            bg="#000000",
            fg="#FFFFFF",
            selectcolor="#333333",
            font=("Arial", 10)
        )
        empleado_radio.grid(row=12, column=0, sticky="w", pady=2)

        # Botón de registro
        registrar_btn = tk.Button(
            form_frame,
            text="📝 Registrar Usuario",
            font=("Arial", 12, "bold"),
            bg="#E50914",
            fg="#FFFFFF",
            activebackground="#B2070F",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.registrar_usuario,
            padx=20,
            pady=10
        )
        registrar_btn.grid(row=13, column=0, pady=20)

        # ✅ CORRECCIÓN: Botón "Volver al Login" con color válido
        volver_btn = tk.Button(
            form_frame,
            text="← Volver al Login",
            font=("Arial", 10),
            bg="#000000",  # Cambiado de "transparent" a "#000000"
            fg="#CCCCCC",
            relief="flat",
            cursor="hand2",
            command=self.destroy,
            bd=0  # Sin borde
        )
        volver_btn.grid(row=14, column=0, pady=10)

        # Configurar bindings para Enter
        for entry in self.entries.values():
            entry.bind("<Return>", lambda e: self.registrar_usuario())

    def validar_campos(self):
        """Validar que todos los campos estén completos y sean válidos"""
        nombre = self.entries['nombre_entry'].get().strip()
        apellido = self.entries['apellido_entry'].get().strip()
        email = self.entries['email_entry'].get().strip()
        password = self.entries['password_entry'].get()
        confirm_password = self.entries['confirm_password_entry'].get()

        # Validar campos vacíos
        if not all([nombre, apellido, email, password, confirm_password]):
            messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
            return False

        # Validar email
        if not self.validar_email(email):
            messagebox.showwarning("Validación", "Por favor ingresa un email válido.")
            self.entries['email_entry'].focus()
            return False

        # Validar contraseñas
        if password != confirm_password:
            messagebox.showwarning("Validación", "Las contraseñas no coinciden.")
            self.entries['password_entry'].delete(0, tk.END)
            self.entries['confirm_password_entry'].delete(0, tk.END)
            self.entries['password_entry'].focus()
            return False

        if len(password) < 6:
            messagebox.showwarning("Validación", "La contraseña debe tener al menos 6 caracteres.")
            self.entries['password_entry'].focus()
            return False

        return True

    def registrar_usuario(self):
        """Registrar nuevo usuario en la base de datos"""
        if not self.validar_campos():
            return

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()

            # Obtener datos del formulario
            nombre = self.entries['nombre_entry'].get().strip()
            apellido = self.entries['apellido_entry'].get().strip()
            email = self.entries['email_entry'].get().strip()
            password = self.entries['password_entry'].get()
            tipo = self.tipo_usuario.get()

            # Verificar si el email ya existe
            cursor.execute("SELECT id_datos FROM DatosIdentificacion WHERE correo = ?", email)
            if cursor.fetchone():
                messagebox.showerror("Error", "Este email ya está registrado.")
                conn.close()
                return

            # Hashear contraseña
            password_hash = self.hash_password(password)

            # Insertar en DatosIdentificacion
            cursor.execute("""
                INSERT INTO DatosIdentificacion (nombre, apellido, correo, contraseña)
                VALUES (?, ?, ?, ?)
            """, nombre, apellido, email, password_hash)

            id_datos = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            # Insertar según el tipo de usuario
            if tipo == "cliente":
                cursor.execute("""
                    INSERT INTO Cliente (metodo_pago, historial_rentas, id_datos)
                    VALUES (?, ?, ?)
                """, "Efectivo", "Ninguna renta previa", id_datos)
                mensaje_exito = "Cliente registrado exitosamente."
            else:
                cursor.execute("""
                    INSERT INTO Empleado (id_datos)
                    VALUES (?)
                """, id_datos)
                mensaje_exito = "Empleado registrado exitosamente."

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", f"{mensaje_exito}\n\nAhora puedes iniciar sesión.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroView(root)
    root.mainloop()