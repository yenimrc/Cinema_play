from datetime import date

class Renta:
    def __init__(self, id_renta=None, id_cliente=None, id_pelicula=None, fecha_renta=None, fecha_limite=None, fecha_devolucion=None, recargo=0.0):
        self.id_renta = id_renta
        self.id_cliente = id_cliente
        self.id_pelicula = id_pelicula
        self.fecha_renta = fecha_renta if fecha_renta else date.today()
        self.fecha_limite = fecha_limite
        self.fecha_devolucion = fecha_devolucion
        self.recargo = recargo

    # Métodos opcionales de utilidad
    def calcular_recargo(self):
        #para calcular el recargo si la pelicula se devuelve despes de la fecha limite.
        if self.fecha_devolucion and self.fecha_devolucion > self.fecha_limite:
            dias_retraso = (self.fecha_devolucion - self.fecha_limite).days
            self.recargo = dias_retraso * 25  #$25 por día de retraso
        else:
            self.recargo = 0.0
        return self.recargo

    def __str__(self):
        return (f"Renta(ID: {self.id_renta}, Cliente: {self.id_cliente}, Película: {self.id_pelicula}, "
                f"Fecha renta: {self.fecha_renta}, Límite: {self.fecha_limite}, "
                f"Devolución: {self.fecha_devolucion}, Recargo: ${self.recargo})")
