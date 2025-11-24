# main.py - Punto de entrada principal de CINEMA PLAY

import tkinter as tk
from tkinter import messagebox
import sys
import os
from VIEWS.menu_principal import MenuPrincipal

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Agregar el directorio VIEWS al path para las importaciones
        current_dir = os.path.dirname(os.path.abspath(__file__))
        views_path = os.path.join(current_dir, 'VIEWS')
        sys.path.append(views_path)
        
        print("🔧 Iniciando CINEMA PLAY...")
        print(f"📁 Directorio actual: {current_dir}")
        print(f"📁 Path VIEWS: {views_path}")
        
        
        
        # Crear instancia de la aplicación principal
        app = MenuPrincipal()
        
        print("✅ Aplicación iniciada correctamente")
        
        # Configurar manejo de excepciones no capturadas
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                # Si el usuario presiona Ctrl+C, salir silenciosamente
                print("👋 Aplicación cerrada por el usuario")
                sys.exit(0)
            else:
                # Mostrar error en messagebox
                error_msg = f"Error no capturado:\n\nTipo: {exc_type.__name__}\nMensaje: {exc_value}"
                print(f"❌ Error crítico: {error_msg}")
                messagebox.showerror("Error Crítico", error_msg)
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
        
        sys.excepthook = handle_exception
        
        # Iniciar el loop principal de la aplicación
        app.mainloop()
        
    except ImportError as e:
        error_msg = f"Error de importación: {e}"
        print(f"❌ {error_msg}")
        messagebox.showerror(
            "Error de Inicialización", 
            f"No se pudieron cargar los módulos necesarios:\n{e}\n\n"
            f"Asegúrate de que todos los archivos .py estén en la carpeta VIEWS/"
        )
    except Exception as e:
        error_msg = f"Error al iniciar la aplicación: {e}"
        print(f"❌ {error_msg}")
        messagebox.showerror(
            "Error Inesperado", 
            f"Ocurrió un error al iniciar la aplicación:\n{e}"
        )

if __name__ == "__main__":
    # Ejecutar la aplicación
    main()

