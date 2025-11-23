
from DAO.clientes_dao import ClienteDAO
from MODELS.clientes import Cliente

class ClienteController:

    @staticmethod
    def listar_clientes():
        return ClienteDAO.obtener_todos()

    @staticmethod
    def crear_cliente(metodo_pago, historial_rentas, id_datos):
        cliente = Cliente(metodo_pago=metodo_pago, historial_rentas=historial_rentas, id_datos=id_datos)
        ClienteDAO.agregar(cliente)

    @staticmethod
    def actualizar_cliente(id_cliente, metodo_pago, historial_rentas, id_datos):
        cliente = Cliente(id_cliente=id_cliente, metodo_pago=metodo_pago, historial_rentas=historial_rentas, id_datos=id_datos)
        ClienteDAO.actualizar(cliente)

    @staticmethod
    def eliminar_cliente(id_cliente):
        ClienteDAO.eliminar(id_cliente)
