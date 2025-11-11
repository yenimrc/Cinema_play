class Pelicula:
    def __init__(self, id_pelicula=None, titulo="", genero="", anio=None, disponible=True, precio_renta=0.0):
        self.id_pelicula = id_pelicula
        self.titulo = titulo
        self.genero = genero
        self.anio = anio
        self.disponible = disponible
        self.precio_renta = precio_renta

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.titulo} ({self.anio}) - {self.genero} - {estado} - ${self.precio_renta:.2f}"

    # Métodos opcionales para actualizar atributos
    def marcar_como_rentada(self):
        """Marca la película como no disponible"""
        self.disponible = False

    def marcar_como_disponible(self):
        """Marca la película como disponible nuevamente"""
        self.disponible = True
