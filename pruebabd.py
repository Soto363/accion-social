import psycopg2

try:
    conn = psycopg2.connect(
        dbname='Inventario_db',
        user='postgres',
        password='1234',
        host='localhost',
        port='5433'
    )
    print("✅ Conexión exitosa")
    conn.close()
except Exception as e:
    print("❌ Error:", e)
