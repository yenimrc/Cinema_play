import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pyodbc

class RentaView(tk.Toplevel):
    def __init__(self, parent, tipo_vista="rentas"):
        super().__init__(parent)
        self.title("🎟️ Sistema de Rentas - CINEMA PLAY")
        self.geometry("1000x600")
        self.configure(bg="#E9EEF3")
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
        self.conn = self.conectar_db()
        
        self.tipo_vista = tipo_vista  # "rentas" o "devoluciones"
        self.crear_interfaz()

    def conectar_db(self):
        """Conectar a la base de datos"""
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
            return None

    def crear_interfaz(self):
        # =======================
        #   HEADER SUPERIOR
        # =======================
        header = tk.Frame(self, bg="#2F3A56", height=60)
        header.pack(fill="x")
        
        titulo_texto = "Sistema de Rentas Activas" if self.tipo_vista == "rentas" else "Registro de Devoluciones"
        tk.Label(
            header,
            text=f"🎟️ {titulo_texto} • CINEMA PLAY",
            bg="#2F3A56",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        # =======================
        #   CONTROLES SUPERIORES
        # =======================
        controles_frame = tk.Frame(self, bg="#E9EEF3")
        controles_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón para cambiar entre vistas
        if self.tipo_vista == "rentas":
            tk.Button(controles_frame,
                     text="📦 Ver Devoluciones",
                     command=self.mostrar_devoluciones,
                     bg="#07329E",
                     fg="white",
                     font=("Segoe UI", 10, "bold"),
                     padx=15,
                     pady=5).pack(side="left", padx=5)
        else:
            tk.Button(controles_frame,
                     text="📋 Ver Rentas Activas",
                     command=self.mostrar_rentas_activas,
                     bg="#E93E00",
                     fg="white",
                     font=("Segoe UI", 10, "bold"),
                     padx=15,
                     pady=5).pack(side="left", padx=5)
        
        # Botón actualizar
        tk.Button(controles_frame,
                 text="🔄 Actualizar",
                 command=self.cargar_datos,
                 bg="#00A86B",
                 fg="white",
                 font=("Segoe UI", 10, "bold"),
                 padx=15,
                 pady=5).pack(side="left", padx=5)

        # =======================
        #   TABLA PRINCIPAL
        # =======================
        tabla_frame = tk.Frame(self, bg="#E9EEF3")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if self.tipo_vista == "rentas":
            columnas = ("ID Renta", "Cliente", "Película", "Fecha Inicio", "Fecha Límite", "Días Restantes")
        else:
            columnas = ("ID Renta", "Cliente", "Película", "Fecha Inicio", "Fecha Devolución", "Estado")

        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=15)

        # Estilo tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading",
                        background="#4B7EFF",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview",
                        font=("Segoe UI", 10),
                        rowheight=25,
                        background="white",
                        fieldbackground="white")

        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            if col in ["ID Renta", "Días Restantes"]:
                self.tabla.column(col, width=100, anchor="center")
            else:
                self.tabla.column(col, width=150, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # =======================
        #   BOTONES DE ACCIÓN
        # =======================
        if self.tipo_vista == "rentas":
            botones_frame = tk.Frame(self, bg="#E9EEF3")
            botones_frame.pack(pady=10)
            
            tk.Button(botones_frame,
                     text="📦 Registrar Devolución",
                     command=self.registrar_devolucion,
                     bg="#07329E",
                     fg="white",
                     font=("Segoe UI", 11, "bold"),
                     padx=20,
                     pady=8).pack(side="left", padx=10)
            
            tk.Button(botones_frame,
                     text="📊 Calcular Recargo",
                     command=self.calcular_recargo,
                     bg="#FF6B00",
                     fg="white",
                     font=("Segoe UI", 11, "bold"),
                     padx=20,
                     pady=8).pack(side="left", padx=10)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Cargar datos según el tipo de vista"""
        if not self.conn:
            messagebox.showerror("Error", "No hay conexión a la base de datos")
            return

        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            cursor = self.conn.cursor()

            if self.tipo_vista == "rentas":
                # Cargar rentas activas
                cursor.execute("""
                    SELECT r.id_renta, di.nombre + ' ' + di.apellido as cliente, 
                           p.nombre as pelicula, r.fecha_inicio, r.fecha_devolucion,
                           DATEDIFF(day, GETDATE(), r.fecha_devolucion) as dias_restantes
                    FROM Renta r
                    JOIN Cliente c ON r.id_cliente = c.id_cliente
                    JOIN DatosIdentificacion di ON c.id_datos = di.id_datos
                    JOIN Pelicula p ON r.id_pelicula = p.id_pelicula
                    WHERE r.estado = 'Activa'
                    ORDER BY r.fecha_devolucion ASC
                """)
                
                rentas = cursor.fetchall()
                for renta in rentas:
                    id_renta, cliente, pelicula, fecha_inicio, fecha_devolucion, dias_restantes = renta
                    
                    # Formatear fechas
                    fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y") if fecha_inicio else "N/A"
                    fecha_devolucion_str = fecha_devolucion.strftime("%d/%m/%Y") if fecha_devolucion else "N/A"
                    
                    # Determinar color según días restantes
                    dias_texto = f"{dias_restantes} días"
                    if dias_restantes < 0:
                        dias_texto = f"⚠️ {abs(dias_restantes)} días de retraso"
                    elif dias_restantes <= 2:
                        dias_texto = f"🔴 {dias_restantes} días"
                    elif dias_restantes <= 5:
                        dias_texto = f"🟡 {dias_restantes} días"
                    else:
                        dias_texto = f"🟢 {dias_restantes} días"
                    
                    self.tabla.insert("", "end", values=(
                        id_renta, cliente, pelicula, fecha_inicio_str, 
                        fecha_devolucion_str, dias_texto
                    ))

            else:
                # Cargar devoluciones (rentas finalizadas)
                cursor.execute("""
                    SELECT r.id_renta, di.nombre + ' ' + di.apellido as cliente, 
                           p.nombre as pelicula, r.fecha_inicio, r.fecha_devolucion, r.estado
                    FROM Renta r
                    JOIN Cliente c ON r.id_cliente = c.id_cliente
                    JOIN DatosIdentificacion di ON c.id_datos = di.id_datos
                    JOIN Pelicula p ON r.id_pelicula = p.id_pelicula
                    WHERE r.estado = 'Devuelto'
                    ORDER BY r.fecha_devolucion DESC
                """)
                
                devoluciones = cursor.fetchall()
                for dev in devoluciones:
                    id_renta, cliente, pelicula, fecha_inicio, fecha_devolucion, estado = dev
                    
                    # Formatear fechas
                    fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y") if fecha_inicio else "N/A"
                    fecha_devolucion_str = fecha_devolucion.strftime("%d/%m/%Y") if fecha_devolucion else "N/A"
                    
                    estado_texto = "✅ Devuelto" if estado == "Devuelto" else estado
                    
                    self.tabla.insert("", "end", values=(
                        id_renta, cliente, pelicula, fecha_inicio_str, 
                        fecha_devolucion_str, estado_texto
                    ))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def registrar_devolucion(self):
        """Registrar devolución de una renta seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una renta para devolver.")
            return

        item = self.tabla.item(seleccion[0])
        valores = item['values']
        id_renta = valores[0]
        cliente = valores[1]
        pelicula = valores[2]

        # Confirmar devolución
        respuesta = messagebox.askyesno(
            "Confirmar Devolución",
            f"¿Está seguro de registrar la devolución?\n\n"
            f"Cliente: {cliente}\n"
            f"Película: {pelicula}"
        )

        if respuesta:
            try:
                cursor = self.conn.cursor()
                
                # Actualizar estado a 'Devuelto' y fecha de devolución a hoy
                cursor.execute("""
                    UPDATE Renta 
                    SET estado = 'Devuelto', fecha_devolucion = GETDATE()
                    WHERE id_renta = ?
                """, id_renta)
                
                self.conn.commit()
                
                messagebox.showinfo("Éxito", f"Devolución registrada correctamente para:\n{cliente} - {pelicula}")
                self.cargar_datos()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar la devolución: {e}")

    def calcular_recargo(self):
        """Calcular recargo por retraso"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione una renta para calcular recargo.")
            return

        item = self.tabla.item(seleccion[0])
        valores = item['values']
        id_renta = valores[0]
        cliente = valores[1]
        pelicula = valores[2]
        dias_texto = valores[5]

        try:
            cursor = self.conn.cursor()
            
            # Obtener información de la renta
            cursor.execute("""
                SELECT r.fecha_devolucion, p.costo_renta
                FROM Renta r
                JOIN Pelicula p ON r.id_pelicula = p.id_pelicula
                WHERE r.id_renta = ?
            """, id_renta)
            
            resultado = cursor.fetchone()
            if resultado:
                fecha_limite, costo_renta = resultado
                dias_retraso = (datetime.now().date() - fecha_limite).days
                
                if dias_retraso > 0:
                    recargo = costo_renta * 0.1 * dias_retraso  # 10% por día de retraso
                    total = costo_renta + recargo
                    
                    messagebox.showinfo(
                        "Cálculo de Recargo",
                        f"Cliente: {cliente}\n"
                        f"Película: {pelicula}\n"
                        f"Días de retraso: {dias_retraso}\n"
                        f"Costo renta: ${costo_renta:.2f}\n"
                        f"Recargo: ${recargo:.2f}\n"
                        f"Total a pagar: ${total:.2f}"
                    )
                else:
                    messagebox.showinfo(
                        "Sin Recargo",
                        f"Cliente: {cliente}\n"
                        f"Película: {pelicula}\n"
                        f"No hay recargo. La renta está al día."
                    )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo calcular el recargo: {e}")

    def mostrar_devoluciones(self):
        """Cambiar a vista de devoluciones"""
        self.destroy()
        RentaView(self.parent, "devoluciones")

    def mostrar_rentas_activas(self):
        """Cambiar a vista de rentas activas"""
        self.destroy()
        RentaView(self.parent, "rentas")

if __name__ == "__main__":
    root = tk.Tk()
    app = RentaView(root)
    app.mainloop()

    