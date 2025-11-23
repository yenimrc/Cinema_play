
from conexion import obtener_conexion
from MODELS.clientes import Cliente

class ClienteDAO:
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        clientes = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Cliente")
            for row in cursor.fetchall():
                clientes.append(Cliente(row[0], row[1], row[2], row[3]))
            conexion.close()
        return clientes

    @staticmethod
    def agregar(cliente):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO Cliente (metodo_pago, historial_rentas, id_datos)
                VALUES (?, ?, ?)
            """, (cliente.metodo_pago, cliente.historial_rentas, cliente.id_datos))
            conexion.commit()
            conexion.close()

    @staticmethod
    def actualizar(cliente):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE Cliente SET metodo_pago=?, historial_rentas=?, id_datos=?
                WHERE id_cliente=?
            """, (cliente.metodo_pago, cliente.historial_rentas, cliente.id_datos, cliente.id_cliente))
            conexion.commit()
            conexion.close()

    @staticmethod
    def eliminar(id_cliente):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Cliente WHERE id_cliente=?", (id_cliente,))
            conexion.commit()
            conexion.close()


