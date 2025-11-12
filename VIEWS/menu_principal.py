# VIEWS/menu_principal.py

import tkinter as tk
from tkinter import messagebox

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        # Cambiando el título de la ventana y los colores de fondo
        self.title("✨ CINEMA PLAY")
        self.geometry("500x400")
        self.config(bg="#0a0a0a")  # Fondo negro profundo para un ambiente cinematográfico

        # Crear imagen de fondo (simulada con un Canvas)
        self.canvas = tk.Canvas(self, width=500, height=400, highlightthickness=0, bg="#0a0a0a")
        self.canvas.pack(fill="both", expand=True)
        
        # --- DISEÑO LLAMATIVO CARACTERÍSTICO DE PELÍCULAS ---
        
        # Fondo con efecto de "pantalla de cine" (gradiente sutil de negro a gris oscuro)
        for y in range(0, 400, 5):
            tono = int(10 + (y / 400) * 40)
            color = f"#{tono:02x}{tono:02x}{tono:02x}"
            self.canvas.create_line(0, y, 500, y, fill=color, width=5)

        
        # Cortina de cine (arcos en las esquinas superiores)
        self.canvas.create_arc(0, 0, 100, 100, start=0, extent=90, fill="#8b0000", outline="#8b0000")  # Rojo oscuro
        self.canvas.create_arc(400, 0, 500, 100, start=90, extent=90, fill="#8b0000", outline="#8b0000")
        
        # Pantalla central con "película proyectada" (rectángulo con líneas horizontales simulando fotogramas)
        self.canvas.create_rectangle(100, 100, 400, 300, fill="#000000", outline="#ffcc00", width=3)
        for i in range(110, 290, 10):
            self.canvas.create_line(110, i, 390, i, fill="#333333", width=1)
        
        # Estrellas de Hollywood (polígonos dorados en las esquinas)
        star_coords = [50, 50, 55, 60, 65, 60, 60, 70, 55, 75, 50, 80, 45, 75, 40, 70, 45, 60, 35, 60]
        self.canvas.create_polygon(star_coords, fill="#ffd700", outline="#ff8c00", width=2)  # Superior izquierda
        self.canvas.create_polygon([x + 400 for x in star_coords], fill="#ffd700", outline="#ff8c00", width=2)  # Superior derecha
        
        # Cámaras de filmación (formas simples con lentes)
        # Izquierda
        self.canvas.create_rectangle(20, 320, 60, 340, fill="#666666", outline="#999999", width=2)
        self.canvas.create_oval(25, 325, 35, 335, fill="#000000", outline="#ffffff", width=1)
        # Derecha
        self.canvas.create_rectangle(440, 320, 480, 340, fill="#666666", outline="#999999", width=2)
        self.canvas.create_oval(445, 325, 455, 335, fill="#000000", outline="#ffffff", width=1)
        
        # Palomitas y refrescos (óvalos y rectángulos coloridos)
        self.canvas.create_oval(80, 350, 100, 370, fill="#ffff00", outline="#ffcc00", width=2)  # Palomitas
        self.canvas.create_rectangle(110, 355, 130, 375, fill="#ff4500", outline="#8b0000", width=2)  # Refresco
        
        # Claqueta gigante en el centro inferior
        self.canvas.create_rectangle(200, 320, 300, 380, fill="#000000", outline="#ffffff", width=4)
        self.canvas.create_line(200, 340, 300, 340, fill="#ffffff", width=6)
        self.canvas.create_text(250, 330, text="CINEMA", fill="#ffffff", font=("Segoe UI", 12, "bold"))
        self.canvas.create_text(250, 350, text="PLAY", fill="#ffffff", font=("Segoe UI", 12, "bold"))
        
        # Luces de foco (círculos amarillos en los bordes)
        self.canvas.create_oval(10, 150, 30, 170, fill="#ffff00", outline="#ffcc00", width=2)
        self.canvas.create_oval(470, 150, 490, 170, fill="#ffff00", outline="#ffcc00", width=2)
        
        # 1. Título de Marca (Dorado/Ámbar con sombra)
        self.canvas.create_text(252, 82, text="🎞 CINEMA PLAY 🍿", fill="#000000", font=("Myanmar Text", 24, "bold"))  # Sombra
        self.canvas.create_text(250, 80, text="🎞 CINEMA PLAY 🍿", fill="#ffc72c", font=("Myanmar Text", 24, "bold"))
        
        # 2. Eslogan
        self.canvas.create_text(250, 120, 
                                text="Tu Próximo Estreno Comienza Aquí", 
                                fill="#cccccc",  # Gris claro
                                font=("Segoe UI", 12))

        # 3. Botón Cliente (Principal - Tono Ámbar/Naranja destacado)
        
        # Usamos un Frame para simular un botón más moderno y grande
        frame_cliente = tk.Frame(self, bg="#ff8c00", bd=0, relief="flat", highlightthickness=0)
        btn_cliente = tk.Button(frame_cliente, text="▶️ Ingresar como cliente", width=30, height=2,
                              bg="#ff8c00", fg="white", font=("Segoe UI", 13, "bold"),
                              command=self.abrir_cliente, relief="flat", bd=0, activebackground="#e67e22")
        btn_cliente.pack(padx=2, pady=2) # Pequeño padding para simular el borde del frame
        
        self.canvas.create_window(250, 200, window=frame_cliente, height=50, width=300)

        # 4. Botón Empleado (Secundario - Tono Gris Oscuro Sobrio)
        
        # Usamos un Frame con borde claro para darle un look "outline"
        frame_empleado = tk.Frame(self, bg="#333333", bd=0, relief="flat", highlightthickness=1, highlightbackground="#555555")
        btn_empleado = tk.Button(frame_empleado, text="🔒 Ingreso como administrador", width=30, height=2,
                               bg="#333333", fg="white", font=("Segoe UI", 11, "bold"),
                               command=self.abrir_empleado, relief="flat", bd=0, activebackground="#222222")
        btn_empleado.pack(padx=2, pady=2)
        
        self.canvas.create_window(250, 270, window=frame_empleado, height=45, width=280)

        # 5. Botón Salir (Discreto en la esquina inferior derecha)
        btn_salir = tk.Button(self, text="Cerrar ✖️", 
                            bg="#0a0a0a", fg="#D00000", font=("Segoe UI", 10),
                            command=self.salir, relief="flat", bd=0, activebackground="#0a0a0a", activeforeground="white")
        self.canvas.create_window(450, 385, window=btn_salir, anchor="se")

    def abrir_cliente(self):
        # Importar aquí para evitar errores de importación circular
        from cliente_view import CatalogoPeliculasView
        self.destroy()
        CatalogoPeliculasView().mainloop()

    def abrir_empleado(self):
        # Importar aquí para evitar errores de importación circular
        from empleado_view import EmpleadoView
        self.destroy()
        EmpleadoView().mainloop()

    def salir(self):
        self.destroy()

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()


