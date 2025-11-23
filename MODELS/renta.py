

from MODELS.pelicula import Pelicula
from datetime import datetime
class Renta(Pelicula):
    def __init__(self, id_pelicula:int, nombre:str, genero:str, duracion:float, costo_renta:float, fecha_inicio:str, fecha_devolucion:str, estado:str):
        super.__init__(self, id_pelicula, nombre, genero, duracion, costo_renta)
        self.fecha_inicio=fecha_inicio
        self.fecha_devolucion=fecha_devolucion
        self.estado=estado
        
