
from conexion import obtener_conexion
from MODELS.empleado import Empleado

class EmpleadoDAO:
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        empleados = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Empleado")
            for row in cursor.fetchall():
                empleados.append(Empleado(row[0], row[1]))
            conexion.close()
        return empleados

    @staticmethod
    def agregar(empleado):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO Empleado (id_datos) VALUES (?)", (empleado.id_datos,))
            conexion.commit()
            conexion.close()

    @staticmethod
    def actualizar(empleado):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("UPDATE Empleado SET id_datos=? WHERE id_empleado=?", (empleado.id_datos, empleado.id_empleado))
            conexion.commit()
            conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Empleado WHERE id_empleado=?", (id_empleado,))
            conexion.commit()
            conexion.close()
