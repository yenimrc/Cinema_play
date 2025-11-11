# VIEWS/menu_principal.py

import tkinter as tk
from tkinter import messagebox
# Importar las vistas
from cliente_view import CatalogoPeliculasView
from empleado_view import EmpleadoView

class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Catálogo de Películas")
        self.geometry("500x400")
        self.config(bg="#1e1e1e")

        # Título
        tk.Label(self, text="🎬 BIENVENIDO AL CATÁLOGO DE PELÍCULAS",
                 bg="#1e1e1e", fg="white", font=("Arial", 14, "bold")).pack(pady=30)

        # Botón Cliente
        tk.Button(self, text="👤 Ingresar como Cliente", width=30, height=2,
                  bg="#007acc", fg="white", font=("Arial", 12, "bold"),
                  command=self.abrir_cliente).pack(pady=20)

        # Botón Empleado
        tk.Button(self, text="🧑‍💼 Ingresar como Empleado", width=30, height=2,
                  bg="#4caf50", fg="white", font=("Arial", 12, "bold"),
                  command=self.abrir_empleado).pack(pady=10)

        # Botón Salir
        tk.Button(self, text="❌ Salir", width=15, bg="#d32f2f", fg="white",
                  command=self.salir).pack(pady=30)

    def abrir_cliente(self):
        messagebox.showinfo("Cliente", "Abrir interfaz del cliente (cliente_view.py)")
        # self.destroy()
        # CatalogoPeliculasView().mainloop()

    def abrir_empleado(self):
        messagebox.showinfo("Empleado", "Abrir interfaz del empleado (empleado_view.py)")
        # self.destroy()
        # EmpleadoView().mainloop()

    def salir(self):
        self.destroy()

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
