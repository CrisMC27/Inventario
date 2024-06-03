import psycopg2
from datetime import date
from tabulate import tabulate
import matplotlib.pyplot as plt

#DESARROLLADORE:
#Cristian Martinez, Daniel Segura, Michael Paez

print()
print("-------------------Bodega de repuestos EL CONSORCIO-------------------")
print("----------------------------------------------------------------------")


#Conexion a la base de datos que esta en un localhost


def conectar():
    try:
        conexion = psycopg2.connect(
            dbname="inventario",
            user="admin",
            password="654321",
            host="localhost",
            port="5432"
        )
        return conexion
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None


#Funcion para consultar los articulos


def consultar_articulos():

    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()

            # Consulta en la base de datos
            consulta = ("SELECT t1.Codigo, t1.Nombre, t1.Descripcion, t1.Cantidad, t1.Precio_Unitario, "
                        "t2.Nombre_proveedor, (SELECT MAX(Fecha_de_entrada) FROM Movimientos "
                        "WHERE Codigo_articulo = t1.Codigo),(SELECT MAX(Fecha_de_salida) FROM Movimientos "
                        "WHERE Codigo_articulo = t1.Codigo) FROM Articulos t1 "
                        "JOIN Proveedores t2 ON t2.Codigo = t1.Proveedor ORDER BY t1.Codigo ASC")
            cursor.execute(consulta)

            # Obtener los resultados de la consulta
            articulos = cursor.fetchall()

            # Mostrar los artículos
            print("        -----------Articulos Disponibles-----------        ")
            print(tabulate(articulos, headers=["Código", "Nombre", "Descripción", "Cantidad", "Precio Unitario",
                                               "Proveedor", "Última fecha de entrada", "Última fecha de Salida"]))

            #Alerta de stock
            for articulo in articulos:
                if articulo[3] < 6:
                    print()
                    print(f"¡Alerta de stock para, {articulo[1]}! Se deberia realizar un pedido para reponer"
                          f" existencias")

            cursor.close()
            conexion.close()
    except psycopg2.Error as e:
        print("Error al consultar los artículos:", e)


#Funcion que registra las salidas de los articulos


def registrar_salida():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()
            codigo = int(input("Ingrese el código del artículo que desea retirar: "))
            cantidad_retirar = int(input("Ingrese la cantidad que desea retirar: "))
            motivo = input("Ingrese el motivo de la salida (venta, traslado interno o devolucion): ")
            fecha_salida = date.today()

            consulta_cantidad = "SELECT Cantidad FROM Articulos WHERE Codigo = %s"
            cursor.execute(consulta_cantidad, (codigo,))
            cantidad_disponible = cursor.fetchone()[0]
            #Se valida la cantidad del articulo
            if cantidad_disponible >= cantidad_retirar:
                # Se actualiza la cantidad del articulo
                nueva_cantidad = cantidad_disponible - cantidad_retirar
                actualizar_salida = "UPDATE Articulos SET Cantidad = %s WHERE Codigo = %s"
                cursor.execute(actualizar_salida, (nueva_cantidad, codigo))
                conexion.commit()
                print("Registro de salida exitoso. Cantidad actualizada.")
            else:
                print("Cantidad no disponible. No se puede realizar la salida.")

            #Se crea el registro de salida a la base de datos
            consulta = ("INSERT INTO Movimientos (codigo_articulo, cantidad_retirada, motivo_salida, "
                        "fecha_de_salida) VALUES (%s, %s, %s, %s)")
            datos = (codigo, cantidad_retirar, motivo, fecha_salida)
            cursor.execute(consulta, datos)
            conexion.commit()

            cursor.close()
            conexion.close()
    except psycopg2.Error as e:
        print("Error al registrar la salida:", e)


#Funcion que registra la entrada de un nuevo articulo


def registrar_entradanueva():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()

            codigo = int(input("Ingrese el codigo del artículo: "))
            nombre = input("Ingrese el nombre del artículo: ")
            descripcion = input("Ingrese una breve descripcion del artículo: ")
            cantidad = int(input("Ingrese la cantidad: "))
            preciou = int(input("Ingrese el precio unitario: "))
            proveedor = int(input("Ingrese el código del proveedor: "))
            fechae = date.today()

            # Insercion de los datos a la base de datos
            consulta = ("INSERT INTO Articulos (Codigo, Nombre, Descripcion, Cantidad, Precio_Unitario, "
                        "Proveedor, Fecha_de_entrada)"
                        " VALUES (%s, %s, %s, %s, %s, %s, %s)")
            datos = (codigo, nombre, descripcion, cantidad, preciou, proveedor, fechae)

            cursor.execute(consulta, datos)
            conexion.commit()

            print("Registro de entrada creado exitosamente.")

            cursor.close()
            conexion.close()
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)


#Funcion que actualiza la cantidad de un articulo existente


def actualizar_entradaexistente():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()

            codigo = int(input("Ingrese el codigo del artículo: "))
            proveedor = input("Ingrese el codigo del proveedor: ")
            cantidad = int(input("Ingrese la cantidad que ingresará: "))
            fecha = date.today()

            # Se verifica si el código de artículo existe en la base de datos
            consulta_existencia = "SELECT COUNT(*) FROM Articulos WHERE Codigo = %s"
            cursor.execute(consulta_existencia, (codigo,))
            if cursor.fetchone()[0] > 0:
                # Se obtiene la cantidad existente en la base de datos
                consulta_cantidad_existente = "SELECT Cantidad FROM Articulos WHERE Codigo = %s"
                cursor.execute(consulta_cantidad_existente, (codigo,))
                cantidad_existente = cursor.fetchone()[0]

                # Se suma la cantidad ingresada mas la que hay en la base de datos
                cantidad_total = cantidad + cantidad_existente

                # Se actualiza la cantidad total del artículo en la base de datos
                actualizar_cantidad = "UPDATE Articulos SET Cantidad = %s WHERE Codigo = %s"
                cursor.execute(actualizar_cantidad, (cantidad_total, codigo))
                conexion.commit()
            else:
                print("El código del artículo no existe.")

            # Insercion de los datos a la base de datos
            consulta = ("INSERT INTO Movimientos (codigo_articulo, cantidad_ingresada, "
                        "codigo_proveedor, fecha_de_entrada)"
                        " VALUES (%s, %s, %s, %s)")
            datos = (codigo, cantidad, proveedor, fecha)

            cursor.execute(consulta, datos)
            conexion.commit()

            print("Actualizacion exitosa!.")

            cursor.close()
            conexion.close()
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)


#Funciones para obtener datos de la base de datos


def obtener_datos():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()
            #Consulta de los articulos y cantidades
            consulta_stock = "SELECT Nombre, Cantidad FROM Articulos"
            cursor.execute(consulta_stock)
            datos_stock = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos_stock
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)


def obtener_datos2():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()
            #Consulta de las ventas totales de cada articulo
            consulta_salida = ("SELECT t2.Nombre, SUM(t1.Cantidad_retirada) AS Total_Vendido "
                               "FROM Movimientos t1 "
                               "JOIN Articulos t2 ON t1.Codigo_articulo = t2.Codigo "
                               "WHERE t1.Motivo_salida = 'venta' "
                               "GROUP BY t2.Nombre "
                               "ORDER BY Total_Vendido DESC")
            cursor.execute(consulta_salida)
            datos_salida = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos_salida
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)


def obtener_datos3():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()
            consulta_salida3 = ("SELECT COUNT (t1.Cantidad_ingresada) AS total_ingresos, "
                               "t2.Nombre FROM Movimientos t1 "
                               "JOIN Articulos t2 ON t1.Codigo_articulo = t2.Codigo "
                               "WHERE t1.Cantidad_ingresada > 0 GROUP BY t2.Nombre")
            cursor.execute(consulta_salida3)
            datos_salida2 = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos_salida2
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)


def obtener_datos4():
    try:
        conexion = conectar()
        if conexion is not None:
            cursor = conexion.cursor()
            consulta_salida = ("SELECT COUNT (t1.Cantidad_retirada) AS total_retirados, "
                               "t2.Nombre "
                               "FROM Movimientos t1 "
                               "JOIN Articulos t2 ON t1.Codigo_articulo = t2.Codigo "
                               "WHERE t1.Cantidad_retirada > 0 GROUP BY t2.Nombre")
            cursor.execute(consulta_salida)
            datos_salida3 = cursor.fetchall()
            cursor.close()
            conexion.close()
            return datos_salida3
    except psycopg2.Error as e:
        print("Error al registrar la entrada:", e)

#Funciones para graficar las diferentes consultas a la base de datos


def grafica1(datos_stock):
    if datos_stock:
        productos = [fila[0] for fila in datos_stock]
        cantidades = [fila[1] for fila in datos_stock]

        plt.bar(productos, cantidades)
        plt.xlabel('Productos')
        plt.ylabel('Cantidades')
        plt.title('Productos y sus cantidades')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos para graficar.")


def grafica2(datos_salida):
    if datos_salida:
        productos = [fila[0] for fila in datos_salida]
        total_vendido = [fila[1] for fila in datos_salida]

        plt.barh(productos, total_vendido)
        plt.xlabel('Cantidad vendida')
        plt.ylabel('Productos')
        plt.title('Cantidad total vendida por articulo')
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos para graficar.")


def grafica3(datos_salida2):
    if datos_salida2:
        productos = [fila[1] for fila in datos_salida2]
        total_ingresados = [fila[0] for fila in datos_salida2]

        plt.barh(productos, total_ingresados)
        plt.xlabel('Cantidades ingresadas')
        plt.ylabel('Productos')
        plt.title('Entradas por producto')
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos para graficar.")


def grafica4(datos_salida3):
    if datos_salida3:
        productos = [fila[1] for fila in datos_salida3]
        total_retirados = [fila[0] for fila in datos_salida3]

        plt.bar(productos, total_retirados)
        plt.xlabel('Productos')
        plt.ylabel('Cantidades retiradas')
        plt.title('Salidas por producto')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos para graficar.")


#Funcion para salir del la aplicación


def salir():
    print("¡Hasta luego!")
    exit()


#Menu de la aplicación(principal)


def menu():
    while True:
        print("\nMenú:")
        print("1. Consultar Artículos")
        print("2. Registrar Salida")
        print("3. Registrar Nuevo Articulo")
        print("4. Actualizar Cantidad de Articulo Existente")
        print("5. Visualizar grafícas")
        print("6. Salir")

        opcion = input("Ingrese el número de la opción que desea ejecutar: ")

        if opcion == "1":
            consultar_articulos()
        elif opcion == "2":
            registrar_salida()
        elif opcion == "3":
            registrar_entradanueva()
        elif opcion == "4":
            actualizar_entradaexistente()
        elif opcion == "5":
            menu_graficas()
        elif opcion == "6":
            salir()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

#Menu de graficas


def menu_graficas():
    while True:
        print("\nMenú de Gráficas:")
        print("1. Gráfico de productos y sus cantidades")
        print("2. Gráfico de cantidad total vendida por artículo")
        print("3. Gráfico de el total de entradas por artículo")
        print("4. Gráfica de total de salidas por artículo")
        print("5. Volver al menú principal")

        opcion = input("Ingrese el número de la opción que desea ejecutar: ")

        if opcion == "1":
            datos_stock = obtener_datos()
            grafica1(datos_stock)
        elif opcion == "2":
            datos_salida = obtener_datos2()
            grafica2(datos_salida)
        elif opcion == "3":
            datos_salida2 = obtener_datos3()
            grafica3(datos_salida2)
        elif opcion == "4":
            datos_salida3 = obtener_datos4()
            grafica4(datos_salida3)
        elif opcion == "5":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    menu()