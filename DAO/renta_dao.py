
from conexion import obtener_conexion
from MODELS.renta import Renta

class RentaDAO:
    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        rentas = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Renta")
            for row in cursor.fetchall():
                rentas.append(Renta(row[0], row[1], row[2], row[3], row[4], row[5]))
            conexion.close()
        return rentas

    @staticmethod
    def agregar(renta):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO Renta (id_cliente, id_pelicula, fecha_inicio, fecha_devolucion, estado)
                VALUES (?, ?, ?, ?, ?)
            """, (renta.id_cliente, renta.id_pelicula, renta.fecha_inicio, renta.fecha_devolucion, renta.estado))
            conexion.commit()
            conexion.close()

    @staticmethod
    def actualizar(renta):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE Renta SET id_cliente=?, id_pelicula=?, fecha_inicio=?, fecha_devolucion=?, estado=?
                WHERE id_renta=?
            """, (renta.id_cliente, renta.id_pelicula, renta.fecha_inicio, renta.fecha_devolucion, renta.estado, renta.id_renta))
            conexion.commit()
            conexion.close()

    @staticmethod
    def eliminar(id_renta):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Renta WHERE id_renta=?", (id_renta,))
            conexion.commit()
            conexion.close()
