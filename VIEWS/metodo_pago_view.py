# VIEWS/metodo_pago_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime
import re

class MetodoPagoView(tk.Toplevel):
    def __init__(self, parent, id_cliente):
        super().__init__(parent)
        self.parent = parent
        self.id_cliente = id_cliente
        self.title("💳 Métodos de Pago - CINEMA PLAY")
        self.geometry("800x600")
        self.configure(bg="#1a1a2e")
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
        self.cargar_info_pago()

    def conectar_db(self):
        """Conectar a la base de datos"""
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self, bg="#E50914", height=70)
        header.pack(fill="x")
        
        tk.Label(
            header,
            text="💳 CONFIGURACIÓN DE PAGOS",
            bg="#E50914",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        
        # Frame principal con pestañas
        main_frame = tk.Frame(self, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear Notebook (pestañas)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)
        
        # Pestaña 1: Método de Pago Principal
        tab_principal = tk.Frame(notebook, bg="#222831")
        notebook.add(tab_principal, text="Método Principal")
        
        # Pestaña 2: Configurar Tarjeta
        tab_tarjeta = tk.Frame(notebook, bg="#222831")
        notebook.add(tab_tarjeta, text="💳 Tarjeta")
        
        # Pestaña 3: Configurar PayPal
        tab_paypal = tk.Frame(notebook, bg="#222831")
        notebook.add(tab_paypal, text="📱 PayPal")
        
        # Cargar contenido de cada pestaña
        self.crear_tab_principal(tab_principal)
        self.crear_tab_tarjeta(tab_tarjeta)
        self.crear_tab_paypal(tab_paypal)
        
        # Footer
        footer = tk.Label(self,
                         text="💡 Tu información de pago se guarda de forma segura",
                         bg="#1a1a2e",
                         fg="#888",
                         font=("Arial", 9))
        footer.pack(side="bottom", pady=10)

    def crear_tab_principal(self, parent):
        """Crear contenido de la pestaña principal"""
        content = tk.Frame(parent, bg="#222831", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(
            content,
            text="MÉTODO DE PAGO ACTUAL",
            bg="#222831",
            fg="#00ADB5",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 20))
        
        # Frame para mostrar info actual
        self.info_frame = tk.Frame(content, bg="#393e46", relief="solid", bd=1)
        self.info_frame.pack(fill="x", pady=(0, 20))
        
        self.info_label = tk.Label(
            self.info_frame,
            text="Cargando información...",
            bg="#393e46",
            fg="white",
            font=("Arial", 11),
            justify="left",
            padx=10,
            pady=10
        )
        self.info_label.pack(fill="both")
        
        # Frame para selección de método
        seleccion_frame = tk.Frame(content, bg="#222831")
        seleccion_frame.pack(fill="x", pady=20)
        
        tk.Label(
            seleccion_frame,
            text="Seleccionar método principal:",
            bg="#222831",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        self.metodo_var = tk.StringVar(value="Tarjeta")
        
        # Opciones
        opciones_frame = tk.Frame(seleccion_frame, bg="#222831")
        opciones_frame.pack(fill="x")
        
        tk.Radiobutton(
            opciones_frame,
            text="💳 Tarjeta de Crédito/Débito",
            variable=self.metodo_var,
            value="Tarjeta",
            bg="#222831",
            fg="white",
            selectcolor="#393e46",
            font=("Arial", 10)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            opciones_frame,
            text="📱 PayPal",
            variable=self.metodo_var,
            value="PayPal",
            bg="#222831",
            fg="white",
            selectcolor="#393e46",
            font=("Arial", 10)
        ).pack(anchor="w", pady=5)
        
        # Botón para guardar cambios
        tk.Button(
            content,
            text="💾 Guardar Configuración",
            command=self.guardar_metodo_principal,
            bg="#00ADB5",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=10)

    def crear_tab_tarjeta(self, parent):
        """Crear contenido de la pestaña de tarjeta"""
        content = tk.Frame(parent, bg="#222831", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(
            content,
            text="CONFIGURAR TARJETA",
            bg="#222831",
            fg="#00ADB5",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 20))
        
        # Número de tarjeta
        tk.Label(
            content,
            text="Número de Tarjeta:",
            bg="#222831",
            fg="white",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(5, 0))
        
        self.tarjeta_numero_entry = tk.Entry(
            content,
            font=("Arial", 11),
            bg="#393e46",
            fg="white",
            insertbackground="white"
        )
        self.tarjeta_numero_entry.pack(fill="x", pady=5)
        self.tarjeta_numero_entry.bind("<KeyRelease>", self.formatear_numero_tarjeta)
        
        # Nombre del titular
        tk.Label(
            content,
            text="Nombre del Titular:",
            bg="#222831",
            fg="white",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(10, 0))
        
        self.tarjeta_nombre_entry = tk.Entry(
            content,
            font=("Arial", 11),
            bg="#393e46",
            fg="white",
            insertbackground="white"
        )
        self.tarjeta_nombre_entry.pack(fill="x", pady=5)
        
        # Fecha de vencimiento y CVV
        fecha_cvv_frame = tk.Frame(content, bg="#222831")
        fecha_cvv_frame.pack(fill="x", pady=10)
        
        # Fecha de vencimiento
        tk.Label(
            fecha_cvv_frame,
            text="Vencimiento (MM/AA):",
            bg="#222831",
            fg="white",
            font=("Arial", 11)
        ).pack(anchor="w", side="left", padx=(0, 20))
        
        self.tarjeta_vencimiento_entry = tk.Entry(
            fecha_cvv_frame,
            font=("Arial", 11),
            bg="#393e46",
            fg="white",
            insertbackground="white",
            width=10
        )
        self.tarjeta_vencimiento_entry.pack(side="left", padx=(0, 40))
        
        # CVV
        tk.Label(
            fecha_cvv_frame,
            text="CVV:",
            bg="#222831",
            fg="white",
            font=("Arial", 11)
        ).pack(side="left", padx=(0, 10))
        
        self.tarjeta_cvv_entry = tk.Entry(
            fecha_cvv_frame,
            font=("Arial", 11),
            bg="#393e46",
            fg="white",
            insertbackground="white",
            show="*",
            width=8
        )
        self.tarjeta_cvv_entry.pack(side="left")
        
        # Botón para guardar tarjeta
        tk.Button(
            content,
            text="💳 Guardar Tarjeta",
            command=self.guardar_tarjeta,
            bg="#00ADB5",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=20)

    def crear_tab_paypal(self, parent):
        """Crear contenido de la pestaña de PayPal"""
        content = tk.Frame(parent, bg="#222831", padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Label(
            content,
            text="CONFIGURAR PAYPAL",
            bg="#222831",
            fg="#00ADB5",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 20))
        
        # Email de PayPal
        tk.Label(
            content,
            text="Email de PayPal:",
            bg="#222831",
            fg="white",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(5, 0))
        
        self.paypal_email_entry = tk.Entry(
            content,
            font=("Arial", 11),
            bg="#393e46",
            fg="white",
            insertbackground="white"
        )
        self.paypal_email_entry.pack(fill="x", pady=5)
        
        # Información
        info_text = (
            "📱 Para usar PayPal:\n"
            "1. Tu email de PayPal debe estar verificado\n"
            "2. Asegúrate de tener fondos suficientes\n"
            "3. Las transacciones son instantáneas"
        )
        
        tk.Label(
            content,
            text=info_text,
            bg="#222831",
            fg="#888",
            font=("Arial", 10),
            justify="left"
        ).pack(anchor="w", pady=20)
        
        # Botón para guardar PayPal
        tk.Button(
            content,
            text="📱 Guardar PayPal",
            command=self.guardar_paypal,
            bg="#0070BA",  # Color azul de PayPal
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        ).pack(pady=10)

    def formatear_numero_tarjeta(self, event=None):
        """Formatear número de tarjeta con espacios"""
        numero = self.tarjeta_numero_entry.get().replace(" ", "")
        if len(numero) > 16:
            numero = numero[:16]
        
        formateado = ' '.join(numero[i:i+4] for i in range(0, len(numero), 4))
        if formateado != self.tarjeta_numero_entry.get():
            self.tarjeta_numero_entry.delete(0, tk.END)
            self.tarjeta_numero_entry.insert(0, formateado)

    def cargar_info_pago(self):
        """Cargar información de pago del cliente"""
        if not self.conn:
            return
            
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT metodo_pago, tarjeta_numero, tarjeta_nombre_titular,
                       tarjeta_vencimiento, tarjeta_cvv, paypal_email,
                       metodo_predeterminado
                FROM Cliente
                WHERE id_cliente = ?
            """, self.id_cliente)
            
            datos = cursor.fetchone()
            
            if datos:
                metodo_pago, tarjeta_numero, tarjeta_nombre, tarjeta_venc, tarjeta_cvv, paypal_email, metodo_pred = datos
                
                # Actualizar método principal
                self.metodo_var.set(metodo_pred if metodo_pred else "Tarjeta")
                
                # Mostrar información actual
                info_text = ""
                if metodo_pago:
                    info_text += f"📋 Método actual: {metodo_pago}\n"
                
                if tarjeta_numero and len(tarjeta_numero) >= 4:
                    info_text += f"💳 Tarjeta: ****{tarjeta_numero[-4:]}\n"
                
                if paypal_email:
                    info_text += f"📱 PayPal: {paypal_email}\n"
                
                self.info_label.config(text=info_text or "No hay información de pago registrada")
                
                # Cargar datos en campos de tarjeta
                if tarjeta_numero:
                    self.tarjeta_numero_entry.delete(0, tk.END)
                    self.tarjeta_numero_entry.insert(0, tarjeta_numero)
                
                if tarjeta_nombre:
                    self.tarjeta_nombre_entry.delete(0, tk.END)
                    self.tarjeta_nombre_entry.insert(0, tarjeta_nombre)
                
                if tarjeta_venc:
                    self.tarjeta_vencimiento_entry.delete(0, tk.END)
                    self.tarjeta_vencimiento_entry.insert(0, tarjeta_venc)
                
                if tarjeta_cvv:
                    self.tarjeta_cvv_entry.delete(0, tk.END)
                    self.tarjeta_cvv_entry.insert(0, tarjeta_cvv)
                
                # Cargar datos en PayPal
                if paypal_email:
                    self.paypal_email_entry.delete(0, tk.END)
                    self.paypal_email_entry.insert(0, paypal_email)
                    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def guardar_metodo_principal(self):
        """Guardar el método de pago principal seleccionado"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Cliente 
                SET metodo_predeterminado = ?
                WHERE id_cliente = ?
            """, self.metodo_var.get(), self.id_cliente)
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Método de pago principal actualizado.")
            self.cargar_info_pago()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def guardar_tarjeta(self):
        """Guardar información de tarjeta"""
        try:
            numero = self.tarjeta_numero_entry.get().replace(" ", "")
            nombre = self.tarjeta_nombre_entry.get().strip()
            vencimiento = self.tarjeta_vencimiento_entry.get().strip()
            cvv = self.tarjeta_cvv_entry.get().strip()
            
            # Validaciones básicas
            if not numero or len(numero) != 16 or not numero.isdigit():
                messagebox.showwarning("Validación", "Número de tarjeta inválido. Debe tener 16 dígitos.")
                return
            
            if not nombre:
                messagebox.showwarning("Validación", "Nombre del titular es requerido.")
                return
            
            if not vencimiento or len(vencimiento) != 5 or vencimiento[2] != '/':
                messagebox.showwarning("Validación", "Formato de vencimiento inválido. Use MM/AA")
                return
            
            if not cvv or len(cvv) != 3 or not cvv.isdigit():
                messagebox.showwarning("Validación", "CVV inválido. Debe tener 3 dígitos.")
                return
            
            # Guardar en base de datos
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Cliente 
                SET tarjeta_numero = ?,
                    tarjeta_nombre_titular = ?,
                    tarjeta_vencimiento = ?,
                    tarjeta_cvv = ?,
                    metodo_pago = 'Tarjeta'
                WHERE id_cliente = ?
            """, numero, nombre, vencimiento, cvv, self.id_cliente)
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Información de tarjeta guardada correctamente.")
            self.cargar_info_pago()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la tarjeta: {e}")

    def guardar_paypal(self):
        """Guardar información de PayPal"""
        try:
            email = self.paypal_email_entry.get().strip()
            
            if not email or '@' not in email or '.' not in email:
                messagebox.showwarning("Validación", "Email de PayPal inválido.")
                return
            
            # Guardar en base de datos
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Cliente 
                SET paypal_email = ?,
                    metodo_pago = 'PayPal'
                WHERE id_cliente = ?
            """, email, self.id_cliente)
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", "Información de PayPal guardada correctamente.")
            self.cargar_info_pago()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar PayPal: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetodoPagoView(root, 1)
    app.mainloop()

    