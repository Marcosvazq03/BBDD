import ConexionSQL
import mysql.connector
import sqlite3
import csv


def insert_into_deportista(id, nombre, sexo, height, weight, mySQL):
    if not mySQL:
        sql = ("INSERT INTO Deportista (`idDeportista`,`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (?, ?, ?, ?, ?)")
    else:
        sql = ("INSERT INTO Deportista (`idDeportista`,`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (%s, %s, %s, %s, %s)")
    values = (str(id), nombre, sexo, str(height), str(weight))
    cur = self.conn.cursor()
    cur.execute(sql, values)
    self.conn.commit()

def crear_BBDD(mySql):
    path = input("Ruta con el archivo csv para rellenar las tablas de ediciones olimpicas: ")
    try:
        with open(path) as csvFile:
            reader = csv.reader(csvFile)
            reader.__next__()
            mismo_athleta = -1
            for athlete in reader:
                if athlete[0] == "1000":
                    break
                print("Atleta", athlete[0])
                if athlete[0] != mismo_athleta:
                    altura = athlete[4]
                    peso = athlete[5]
                    if athlete[4] == 'NA':
                        altura = 0
                    if athlete[5] == 'NA':
                        peso = 0
                    insert_into_deportista(athlete[0], athlete[1], athlete[2], altura, peso, mySql)
                    mismo_athleta = athlete[0]
                id_deporte = self.insertar_deporte(athlete[12], mySql)
                id_equipo = self.insertar_equipo(athlete[6], athlete[7], mySql)
                id_olimpiada = self.insertar_olimpiada(athlete[8], athlete[9], athlete[10], athlete[11], mySql)
                id_evento = self.insertar_evento(athlete[13], id_deporte, id_olimpiada, mySql)
                edad = athlete[3]
                if athlete[3] == 'NA':
                    edad = -1
                self.__insert_into_participacion(athlete[0], id_evento, id_equipo, athlete[14], edad, mySql)
        self.conn.close()
        print("La carga de la información se ha realizado correctamente.")
    except FileNotFoundError:
        print("El archivo csv no existe")
    except Exception:
        print("Ha ocurrido algún error en la carga.")

host = "localhost"
user = "admin"
password = "password"
database = "ediciones_olimpicas"

resp = -1

while resp != 0:

    resp = int(input("""
            1.  Crear BBDD MySql
            2.  Crear BBDD SQLite
            3.  Listado de deportistas en diferentes deportes
            4.  Listado de deportistas participantes
            5.  Modificar medalla deportista
            6.  Añadir deportista/participación
            7.  Eliminar participación
            0.  Salir del programa.
        """))
    if resp == 1:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)

        #Borrar contenido
        dbConn = mysql.connector.connect(user=user, password=password, host=host)
        cursor = dbConn.cursor(dictionary=True)
        with open("Datos_Olimpiadas/ediciones_olimpicas.sql", "r") as f:
            result_iterator = cursor.execute(f.read(), multi=True)
            for res in result_iterator:
                print("Running query: ", res)
            dbConn.commit()
        cursor.close()
        dbConn.close()

        crear_BBDD(True)
    if resp == 2:
        conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")

        #Borrar contenido
        cursor = conn.cursor()
        with open("Datos_Olimpiadas/ediciones_olimpicas.db.sql", "r") as f:
            cursor.executescript(f.read())

        crear_BBDD(False)
    if resp == 3:
        connSQL.listar_deporistas_participan_diferentes_deportes(user, password, host, database)
    if resp == 4:
        connSQL.listar_deportistas_que_participan(user, password, host, database)
    if resp == 5:
        connSQL.modificar_medalla_deportista(user, password, host, database)
    if resp == 6:
        connSQL.aniadir_deportista_participacion(user, password, host, database)
    if resp == 7:
        connSQL.eliminar_participacion(user, password, host, database)
