# Prueba de conexión simple
import pyodbc

def test_connection():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-N1LR75PN;" # Nombre de tu servidor
            "DATABASE=Cinema;" # Nombre de tu base de datos
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Prueba de consulta
        cursor.execute("SELECT COUNT(*) FROM Peliculas")
        count = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa. Películas en BD: {count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    test_connection()