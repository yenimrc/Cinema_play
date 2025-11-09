import flet as ft

def main(page: ft.Page):
    page.title = "🎞 Cinema Play 🎞"
    page.bgcolor = ft.colors.BLUE_100
    page.scroll = "auto"

    # Imagen decorativa
    img = ft.Image(
        src="img/imagen.jpg",
        width=500,
        height=400,
        fit=ft.ImageFit.CONTAIN, 
    )

    # Título principal
    titulo = ft.Text(
        "🎬 Cinema Play",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLACK,
        text_align="center"
    )

    # Subtítulos
    subtitulo = ft.Column([
        ft.Text(
            "Tu tienda de renta de películas favorita.",
            size=22,
            color=ft.colors.BLACK,
            text_align="center"
        ),
        ft.Text(
            "Descubre una amplia selección de estrenos en línea.",
            size=18,
            color=ft.colors.BLACK,
            text_align="center"
        ),
        ft.Text(
            "¡Disfruta de una noche de cine en casa con amigos y familiares! 🍿",
            size=18,
            color=ft.colors.BLACK,
            text_align="center"
        )
    ], horizontal_alignment="center")

    # Botón con acción
    def on_click(e):
        page.dialog = ft.AlertDialog(
            title=ft.Text("¡Bienvenido!"),
            content=ft.Text("Gracias por comenzar tu experiencia con Cinema Play 🎉"),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: page.dialog.open(False))],
        )
        page.dialog.open = True
        page.update()

    boton = ft.ElevatedButton(
        text="Comenzar 🎬",
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            padding=20
        )
    )

    # Layout general
    page.add(
        ft.Column(
            [titulo, img, subtitulo, boton],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30
        )
    )

ft.app(target=main)

#archivo de diseño de interfaz