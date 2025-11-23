import pyodbc

try:
    # Cadena de conexión
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=cineplus;"
        "Trusted_Connection=yes;"
    )

    cursor = conn.cursor()
    print("✅ Conexión exitosa a SQL Server")
    print("Conectado a la base  de datos ")


except Exception as e:
    print("❌ Error al conectar:", e)

finally:
    conn.close()
