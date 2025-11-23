

from DAO.pelicula_dao import PeliculaDAO
from MODELS.pelicula import Pelicula

class PeliculaController:

    @staticmethod
    def listar_peliculas():
        return PeliculaDAO.obtener_todas()

    @staticmethod
    def crear_pelicula(nombre, genero, duracion, costo_renta):
        pelicula = Pelicula(nombre=nombre, genero=genero, duracion=duracion, costo_renta=costo_renta)
        PeliculaDAO.agregar(pelicula)

    @staticmethod
    def actualizar_pelicula(id_pelicula, nombre, genero, duracion, costo_renta):
        pelicula = Pelicula(id_pelicula=id_pelicula, nombre=nombre, genero=genero, duracion=duracion, costo_renta=costo_renta)
        PeliculaDAO.actualizar(pelicula)

    @staticmethod
    def eliminar_pelicula(id_pelicula):
        PeliculaDAO.eliminar(id_pelicula)
