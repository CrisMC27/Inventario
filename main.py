# Importar las herramientas necesarias para conectarse a la base de datos,
# realizar consultas SQL, mostrar tablas y crear gráficas.

from connection import establecer_conexion, cerrar_conexion#Se importa el archivo connection
import psycopg2 #Libreria para conectar a la base de datos
from tabulate import tabulate #Libreria para mostrar tablas de datos en la consola
import matplotlib.pyplot as plt #Libreria para generar gráficas

# Definir los encabezados globalmente
headers = ["Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]


def ejecutar_consulta(consulta):
    # Establecer una conexión a la base de datos.

    conexion, cursor = establecer_conexion()

    if conexion:
        try:
            # Ejecutar la consulta SQL para obtener información de la base de datos.
            cursor.execute(consulta)

            # Obtener los resultados de la consulta.
            resultados = cursor.fetchall()

            # Devolver los resultados para su posterior uso.
            return resultados
        except psycopg2.Error as e:
            # Manejar cualquier error que ocurra al ejecutar la consulta.
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            # Cerrar la conexión a la base de datos cuando hayamos terminado.
            cerrar_conexion(conexion, cursor)
    else:
        # Manejar el caso en el que no se pueda establecer una conexión a la base de datos.
        print("No se pudo establecer la conexión a la base de datos.")

# Función para mostrar las calificaciones de los estudiantes en una materia específica.


def listar_estudiantes():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        # Consulta SQL para obtener las calificaciones de la materia seleccionada.
        consulta_sql = (f"select mat.mat_nombre, est.est_nombres, est.est_apellidos, "
                        f"cal.cal_investigacion as investigacion, cal.cal_taller as taller, "
                        f"cal.cal_quiz as quiz, cal.cal_parcial as parcial, "
                        f"est.est_identificacion from \"Calificaciones\" cal inner join \"Estudiantes\" "
                        f"est on cal.est_id = est.est_id inner join \"Materias\" mat ON cal.mat_id = "
                        f"mat.mat_id where mat.mat_id = {opcion_materia}")

        # Ejecutar la consulta SQL y obtener los resultados.
        resultados = ejecutar_consulta(consulta_sql)

        # Comprobar si se obtuvieron resultados de la consulta.
        if resultados:
            # Mostrar el encabezado de la tabla de calificaciones.
            print(f"\n\n\n-----------------------------  Calificaciones de la materia {resultados[0][0]} ------------------------------------------\n\n\n")

            # Definir los encabezados de la tabla.
            headers = ["Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]

            # Inicializar una lista para almacenar los datos de los estudiantes.
            data = []

            # Calcular el promedio de cada estudiante y agregarlo a la lista de datos.
            for fila in resultados:
                promedio = 0
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4
                data.append([fila[7], fila[2], fila[1], fila[3], fila[4], fila[5], fila[6], promedio])

            # Mostrar la tabla de calificaciones.
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")


# Función para mostrar las mejores calificaciones de los estudiantes en una materia específica.

def mejores_estudiantes():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        # Consulta SQL para obtener las mejores calificaciones en la materia seleccionada.
        consulta_sql = f"""
            SELECT mat.mat_nombre, est.est_nombres, est.est_apellidos, CAST(cal.cal_investigacion AS FLOAT) AS investigacion,
            CAST(cal.cal_taller AS FLOAT) AS taller,
            CAST(cal.cal_quiz AS FLOAT) AS quiz,
            CAST(cal.cal_parcial AS FLOAT) AS parcial,
            est.est_identificacion
            FROM "Calificaciones" cal
            INNER JOIN "Estudiantes" est ON cal.est_id = est.est_id
            INNER JOIN "Materias" mat ON cal.mat_id = mat.mat_id
            WHERE mat.mat_id = {opcion_materia}
            ORDER BY (cal.cal_investigacion + cal.cal_taller + cal.cal_quiz + cal.cal_parcial) / 4 DESC
            LIMIT 10;
        """
        resultados = ejecutar_consulta(consulta_sql)
        if resultados:
            # Ordenar los resultados por promedio de manera descendente y tomar los 10 mejores.
            resultados_ordenados = sorted(resultados, key=lambda x: (x[3] + x[4] + x[5] + x[6]) / 4, reverse=True)[:10]
            print(f"\n\n\n-----------------------------  Mejores Calificaciones de la materia {resultados[0][0]} ------------------------------------------\n\n\n")
            headers = ["Puesto", "Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]
            data = []
            cont = 0
            for fila in resultados_ordenados:
                cont += 1
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4
                data.append([cont, fila[7], fila[2], fila[1], fila[3], fila[4], fila[5], fila[6], promedio])

            # Mostrar la tabla de las mejores calificaciones.
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")


# Función para mostrar las peores calificaciones de los estudiantes en una materia específica.

def peores_estudiantes():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        #Consulta SQL para obtener las peores calificaciones en la materia seleccionada.
        consulta_sql = f"""
            SELECT mat.mat_nombre, est.est_nombres, est.est_apellidos, CAST(cal.cal_investigacion AS FLOAT) AS investigacion,
            CAST(cal.cal_taller AS FLOAT) AS taller,
            CAST(cal.cal_quiz AS FLOAT) AS quiz,
            CAST(cal.cal_parcial AS FLOAT) AS parcial,
            est.est_identificacion
            FROM "Calificaciones" cal
            INNER JOIN "Estudiantes" est ON cal.est_id = est.est_id
            INNER JOIN "Materias" mat ON cal.mat_id = mat.mat_id
            WHERE mat.mat_id = {opcion_materia}
            ORDER BY (cal.cal_investigacion + cal.cal_taller + cal.cal_quiz + cal.cal_parcial) / 4 ASC
            LIMIT 5;
        """
        resultados = ejecutar_consulta(consulta_sql)
        if resultados:
            # Ordenar los resultados por promedio de manera ascendente y tomar los 5 peores.
            resultados_ordenados = sorted(resultados, key=lambda x: (x[3] + x[4] + x[5] + x[6]) / 4)[:5]
            print(f"\n\n\n-----------------------------  Peores Calificaciones de la materia {resultados[0][0]} ------------------------------------------\n\n\n")
            headers = ["Puesto", "Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]
            data = []
            cont = 0
            for fila in resultados_ordenados:
                cont += 1
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4
                data.append([cont, fila[7], fila[2], fila[1], fila[3], fila[4], fila[5], fila[6], promedio])

            # Mostrar la tabla de las peores calificaciones utilizando el formato "fancy_grid".
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")

# Función para mostrar una lista de estudiantes aprobados y no aprobados en una materia específica.

def estudiantes_aprobados_y_reprobados():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        # consulta SQL para obtener las calificaciones de la materia seleccionada.
        consulta_sql = f"select mat.mat_nombre, est.est_nombres, est.est_apellidos, cal.cal_investigacion as investigacion, cal.cal_taller as taller, cal.cal_quiz as quiz, cal.cal_parcial as parcial, est.est_identificacion from \"Calificaciones\" cal inner join \"Estudiantes\" est on cal.est_id = est.est_id inner join \"Materias\" mat ON cal.mat_id = mat.mat_id where mat.mat_id = {opcion_materia}"

        # Ejecutar la consulta SQL y obtener los resultados.
        resultados = ejecutar_consulta(consulta_sql)
        if resultados:
            print(f"\n\n\n-----------------------------  Listado de aprobados y No aprobados de la materia {resultados[0][0]} ------------------------------------------\n")

            # Crear dos listas para estudiantes con promedio menor a 3 y mayor o igual a 3.
            estudiantes_promedio_menor_3 = []
            estudiantes_promedio_mayor_igual_3 = []

            # Recorrer los resultados y calcular el promedio de cada estudiante.
            for fila in resultados:
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4

                if promedio < 3:
                    estudiantes_promedio_menor_3.append([fila[7], fila[2], fila[1], fila[3], fila[4], fila[5], fila[6], promedio])
                else:
                    estudiantes_promedio_mayor_igual_3.append([fila[7], fila[2], fila[1], fila[3], fila[4], fila[5], fila[6], promedio])

            # Mostrar las tablas para estudiantes con promedio menor a 3 y mayor o igual a 3, si las hay.
            if estudiantes_promedio_menor_3:
                headers = ["Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]
                print(f"\n\n\n-----------------------------  Listado de No aprobados de la materia {resultados[0][0]} ------------------------------------------\n\n\n")
                print(tabulate(estudiantes_promedio_menor_3, headers=headers, tablefmt="fancy_grid"))

            if estudiantes_promedio_mayor_igual_3:
                headers = ["Identificación", "Apellido", "Nombre", "Investigación", "Taller", "Quiz", "Parcial", "Promedio"]
                print(f"\n\n\n-----------------------------  Listado de aprobados de la materia {resultados[0][0]} ------------------------------------------\n\n\n")
                print(tabulate(estudiantes_promedio_mayor_igual_3, headers=headers, tablefmt="fancy_grid"))
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")

# Función para generar estadísticas de calificaciones en una materia específica.

def generar_estadisticas():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        # Consulta SQL para obtener las calificaciones de la materia seleccionada.
        consulta_sql = f"select mat.mat_nombre, est.est_nombres, est.est_apellidos, cal.cal_investigacion as investigacion, cal.cal_taller as taller, cal.cal_quiz as quiz, cal.cal_parcial as parcial, est.est_identificacion from \"Calificaciones\" cal inner join \"Estudiantes\" est on cal.est_id = est.est_id inner join \"Materias\" mat ON cal.mat_id = mat.mat_id where mat.mat_id = {opcion_materia}"

        # Ejecutar la consulta SQL y obtener los resultados.
        resultados = ejecutar_consulta(consulta_sql)
        if resultados:
            # Inicializar variables para estadísticas.
            promedios = []
            cantidad_alumnos = len(resultados)
            promedio_mas_alto = float('-inf')
            promedio_mas_bajo = float('inf')
            aprobados = 0
            desaprobados = 0

            # Recorrer los resultados y calcular el promedio de cada estudiante.
            for fila in resultados:
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4
                promedios.append(promedio)

                # Actualizar promedio más alto y más bajo.
                promedio_mas_alto = max(promedio_mas_alto, promedio)
                promedio_mas_bajo = min(promedio_mas_bajo, promedio)

                # Contar aprobados y desaprobados (suponiendo que 3 es el criterio de aprobación).
                if promedio >= 3:
                    aprobados += 1
                else:
                    desaprobados += 1

            # Calcular el promedio del curso.
            promedio_curso = sum(promedios) / cantidad_alumnos

            # Mostrar estadísticas.
            print(f"\n\n\n------------------ Estadísticas para la materia {resultados[0][0]} ------------------\n\n\n")
            print(f"Cantidad de alumnos: {cantidad_alumnos}")
            print(f"Promedio del curso: {promedio_curso:.2f}")
            print(f"Promedio más alto: {promedio_mas_alto:.2f}")
            print(f"Promedio más bajo: {promedio_mas_bajo:.2f}")
            print(f"Cantidad de estudiantes aprobados: {aprobados}")
            print(f"Cantidad de estudiantes desaprobados: {desaprobados}\n\n\n")
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")


# Función para generar gráficas de estadísticas de calificaciones en una materia específica.

def generar_graficas():
    # Mostrar opciones de materias para que el usuario elija.
    print("Seleccione la materia que desea ver:")
    print("1. Matemáticas")
    print("2. Historia")
    print("3. Ciencias")

    # Solicitar al usuario que ingrese el número de la materia.
    opcion_materia = input("Ingrese el número de la materia: ")

    # Comprobar si el usuario ingresó un número válido de materia.
    if opcion_materia == '1' or opcion_materia == '2' or opcion_materia == '3':
        # Construir una consulta SQL para obtener las calificaciones de la materia seleccionada.
        consulta_sql = f"select mat.mat_nombre, est.est_nombres, est.est_apellidos, cal.cal_investigacion as investigacion, cal.cal_taller as taller, cal.cal_quiz as quiz, cal.cal_parcial as parcial, est.est_identificacion from \"Calificaciones\" cal inner join \"Estudiantes\" est on cal.est_id = est.est_id inner join \"Materias\" mat ON cal.mat_id = mat.mat_id where mat.mat_id = {opcion_materia}"

        # Ejecutar la consulta SQL y obtener los resultados.
        resultados = ejecutar_consulta(consulta_sql)
        if resultados:
            # Inicializar variables para estadísticas.
            promedios = []
            promedio_mas_alto = float('-inf')
            promedio_mas_bajo = float('inf')
            aprobados = 0
            desaprobados = 0

            # Recorrer los resultados y calcular el promedio de cada estudiante.
            for fila in resultados:
                promedio = (fila[3] + fila[4] + fila[5] + fila[6]) / 4
                promedios.append(promedio)

                # Actualizar promedio más alto y más bajo.
                promedio_mas_alto = max(promedio_mas_alto, promedio)
                promedio_mas_bajo = min(promedio_mas_bajo, promedio)

                # Contar aprobados y desaprobados (suponiendo que 3 es el criterio de aprobación).
                if promedio >= 3:
                    aprobados += 1
                else:
                    desaprobados += 1

            # Gráfica de histograma de promedios.
            plt.hist(promedios, bins=10, edgecolor='k')
            plt.xlabel('Promedio')
            plt.ylabel('Cantidad de Estudiantes Materia')
            plt.title('Histograma de Promedios')
            plt.show()

            # Gráfica de pastel para aprobados y desaprobados.
            labels = ['Aprobados', 'Desaprobados']
            sizes = [aprobados, desaprobados]
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')  # Proporción de aspecto igual asegura que la gráfica sea un círculo.
            plt.title('Porcentaje de Aprobados y Desaprobados')
            plt.show()
        else:
            print("No se obtuvieron resultados.")
    else:
        print("Opción no válida. Intente nuevamente")

def menu():
    while True:
        print("Menu:")
        print("1. Listar estudiantes y calcular nota promedio.")
        print("2. Listar los 10 mejores estudiantes.")
        print("3. Listar los 5 peores estudiantes.")
        print("4. Listar estudiantes aprobados y reprobados.")
        print("5. Generar estadísticas.")
        print("6. Generar gráficas.")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            listar_estudiantes()
        elif opcion == '2':
            mejores_estudiantes()
        elif opcion == '3':
            peores_estudiantes()
        elif opcion == '4':
            estudiantes_aprobados_y_reprobados()
        elif opcion == '5':
            generar_estadisticas()
        elif opcion == '6':
            generar_graficas()
        elif opcion == '7':
            print("\n\n\nSaliendo del programa.\n\n\n")
            break
        else:
            print("\n\n\nOpción no válida. Intente nuevamente.\n\n\n")

if __name__ == "__main__":
    # Establecer la conexión a la base de datos desde el archivo de conexión.
    conexion, cursor = establecer_conexion()

    if conexion:
        try:
            menu()
        finally:
            # Cerrar la conexión al salir del programa.
            cerrar_conexion(conexion, cursor)
    else:
        print("No se pudo establecer la conexión a la base de datos.")