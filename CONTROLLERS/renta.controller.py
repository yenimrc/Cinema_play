
from DAO.renta_dao import RentaDAO
from MODELS.renta import Renta

class RentaController:

    @staticmethod
    def listar_rentas():
        return RentaDAO.obtener_todas()

    @staticmethod
    def crear_renta(id_cliente, id_pelicula, fecha_inicio, fecha_devolucion, estado):
        renta = Renta(id_cliente=id_cliente, id_pelicula=id_pelicula, fecha_inicio=fecha_inicio, fecha_devolucion=fecha_devolucion, estado=estado)
        RentaDAO.agregar(renta)

    @staticmethod
    def actualizar_renta(id_renta, id_cliente, id_pelicula, fecha_inicio, fecha_devolucion, estado):
        renta = Renta(id_renta=id_renta, id_cliente=id_cliente, id_pelicula=id_pelicula, fecha_inicio=fecha_inicio, fecha_devolucion=fecha_devolucion, estado=estado)
        RentaDAO.actualizar(renta)

    @staticmethod
    def eliminar_renta(id_renta):
        RentaDAO.eliminar(id_renta)
