import flet as ft

def main(page: ft.Page):
    #se define el nombre de la pagina y el color de fondo
    page.title = " 🎞Cinema Play🎞"
    page.bgcolor = "BLUE_50"

    #para poner una imagen
    img = ft.Image(
        src="interfaz/.venv/disenio/img/imagen.jpg",
        width=500,
        height=400,
        fit=ft.ImageFit.CONTAIN, 
    )

    #para insertar los datos
    titulo = ft.Text("🎬 Cinema Play", size=30, weight="bold", color="black")
    subtitulo = ft.Column([
    ft.Text("Tu tienda de renta de películas favorita. Descubre una amplía selección de estrenos en línea.", size=20, color="Black"),
    ft.Text("¡Disfruta de una noche de cine en casa con amigos y familiares! 🍿🍿", size=20, color="Black") ], 
    horizontal_alignment="center")

    #se inserta un boton
    boton = ft.ElevatedButton("Haz clic aquí para comenzar!!!")

    #para que aparezcan los elementos que insertamos anteriormente
    page.add(
        ft.Column(
            [titulo, img, subtitulo, boton],
            alignment="center",
            horizontal_alignment="center"
        )
    )

ft.app(target=main)

#archivo de diseño de interfaz