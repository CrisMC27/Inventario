import psycopg2


def establecer_conexion():
    try:
        # Establece la conexión a la base de datos.
        conn = psycopg2.connect(
            host="dpg-cnkrn7acn0vc73d8h5qg-a.oregon-postgres.render.com",
            database="estilos_lenguajes_gquf",
            user="estilos_lenguajes_user",
            password="AySEAHTIODoZfMJLOhALi9duvcSGQ4Ot"
        )

        cursor = conn.cursor()
        return conn, cursor
    except psycopg2.Error as e:
        # Muestra el mensaje en caso de no poderse conectar a la base de datos
        print(f"Error al conectar a la base de datos: {e}")
        return None, None

# Función para cerrar la conexión.


def cerrar_conexion(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()