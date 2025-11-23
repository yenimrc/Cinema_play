
from DAO.empleado_dao import EmpleadoDAO
from MODELS.empleado import Empleado

class EmpleadoController:

    @staticmethod
    def listar_empleados():
        return EmpleadoDAO.obtener_todos()

    @staticmethod
    def crear_empleado(id_datos):
        empleado = Empleado(id_datos=id_datos)
        EmpleadoDAO.agregar(empleado)

    @staticmethod
    def actualizar_empleado(id_empleado, id_datos):
        empleado = Empleado(id_empleado=id_empleado, id_datos=id_datos)
        EmpleadoDAO.actualizar(empleado)

    @staticmethod
    def eliminar_empleado(id_empleado):
        EmpleadoDAO.eliminar(id_empleado)
