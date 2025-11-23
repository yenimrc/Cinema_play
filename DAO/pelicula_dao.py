
from conexion import obtener_conexion
from MODELS.pelicula import Pelicula

class PeliculaDAO:
    @staticmethod
    def obtener_todas():
        conexion = obtener_conexion()
        peliculas = []
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Pelicula")
            for row in cursor.fetchall():
                peliculas.append(Pelicula(row[0], row[1], row[2], row[3], row[4]))
            conexion.close()
        return peliculas

    @staticmethod
    def agregar(pelicula):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO Pelicula (nombre, genero, duracion, costo_renta)
                VALUES (?, ?, ?, ?)
            """, (pelicula.nombre, pelicula.genero, pelicula.duracion, pelicula.costo_renta))
            conexion.commit()
            conexion.close()

    @staticmethod
    def actualizar(pelicula):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE Pelicula SET nombre=?, genero=?, duracion=?, costo_renta=?
                WHERE id_pelicula=?
            """, (pelicula.nombre, pelicula.genero, pelicula.duracion, pelicula.costo_renta, pelicula.id_pelicula))
            conexion.commit()
            conexion.close()

    @staticmethod
    def eliminar(id_pelicula):
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Pelicula WHERE id_pelicula=?", (id_pelicula,))
            conexion.commit()
            conexion.close()
