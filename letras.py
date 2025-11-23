import tkinter as tk
import tkinter.font as tkFont

# 1. Configuración inicial
root = tk.Tk()
root.title("Vista Previa de Tipos de Letra (Tkinter)")

# 2. Obtener la lista de familias de fuentes
# (Esta es la línea que ya tenías)
font_families = tkFont.families()

# 3. Limitar la lista a los primeros 50
max_fonts = 300 #número máximo de fuentes a mostrar
preview_fonts = font_families[:max_fonts]

# 4. Crear un contenedor con barra de desplazamiento
# Usamos un Canvas para poder desplazar la lista si es muy larga
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(main_frame)
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# 5. Iterar y crear las etiquetas de vista previa
example_text = "Vista Previa 123 - Hola Mundo"
label_config = {"size": 12}

for i, font_name in enumerate(preview_fonts):
    try:
        # Crea el objeto Font
        font_obj = tkFont.Font(family=font_name, **label_config)
        
        # Crea la etiqueta (Label)
        label = tk.Label(
            scrollable_frame,
            text=f"({i+1}) {font_name}: {example_text}",
            font=font_obj,
            anchor='w' # Alinea el texto a la izquierda
        )
        # Empaqueta la etiqueta en el frame con algo de relleno
        label.pack(fill=tk.X, pady=2, padx=5)
    except tk.TclError:
        # En caso de que haya un error al cargar una fuente (raro pero posible)
        error_label = tk.Label(
            scrollable_frame,
            text=f"({i+1}) {font_name}: ERROR al cargar la fuente.",
            fg="red",
            anchor='w'
        )
        error_label.pack(fill=tk.X, pady=2, padx=5)

# 6. Ejecutar la ventana principal
root.mainloop()