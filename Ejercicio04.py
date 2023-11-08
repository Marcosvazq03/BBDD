import mysql.connector
import sqlite3
import csv


def exist_element(sql, values):
    cur = conn.cursor()
    cur.execute(sql, values)
    row = cur.fetchone()
    if row is not None:
        return row[0]
    return -1

def exist_deporte(deporte, mySQL):
    if not mySQL:
        sql = "SELECT id_deporte from Deporte where nombre = ?"
    else:
        sql = "SELECT id_deporte from Deporte where nombre = %s"
    return exist_element(sql, (deporte, ))

def exist_evento(evento, id_deporte, id_olimpiada, mySQL):
    if not mySQL:
        sql = "SELECT id_evento from Evento where nombre = ? AND id_deporte = ? AND id_olimpiada = ?"
    else:
        sql = "SELECT id_evento from Evento where nombre = %s AND id_deporte = %s AND id_olimpiada = %s"
    return exist_element(sql, (evento, id_deporte, id_olimpiada))

def exist_olimpiadas(year, season, mySQL):
    if not mySQL:
        sql = "SELECT id_olimpiada from Olimpiada where anio = ? AND temporada = ?"
    else:
        sql = "SELECT id_olimpiada from Olimpiada where anio = %s AND temporada = %s"
    return exist_element(sql, (year, season))

def exist_equipo(equipo, noc, mySQL):
    if not mySQL:
        sql = "SELECT id_equipo from Equipo where nombre = ? AND iniciales = ?"
    else:
        sql = "SELECT id_equipo from Equipo where nombre = %s AND iniciales = %s"
    return exist_element(sql, (equipo, noc))

def insert_into_deportista(id, nombre, sexo, weight, height, mySQL):
    if not mySQL:
        sql = ("INSERT INTO Deportista (`id_deportista`,`nombre`,`sexo`,`peso`,`altura`) VALUES (?, ?, ?, ?, ?)")
    else:
        sql = ("INSERT INTO Deportista (`id_deportista`,`nombre`,`sexo`,`peso`,`altura`) VALUES (%s, %s, %s, %s, %s)")
    values = (str(id), nombre, sexo, str(weight), str(height))
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

def insert_into_deporte(deporte, mySQL):
    if not mySQL:
        sql = "INSERT INTO Deporte (`nombre`) VALUES (?)"
    else:
        sql = "INSERT INTO Deporte (`nombre`) VALUES (%s)"
    cur = conn.cursor()
    cur.execute(sql, (deporte,))
    id = cur.lastrowid
    conn.commit()
    return id

def insert_into_equipo(equipo, noc, mySQL):
    if not mySQL:
        sql = "INSERT INTO Equipo (`nombre`, `iniciales`) VALUES (?, ?)"
    else:
        sql = "INSERT INTO Equipo (`nombre`, `iniciales`) VALUES (%s, %s)"
    values = (equipo, noc)
    cur = conn.cursor()
    cur.execute(sql, values)
    id = cur.lastrowid
    conn.commit()
    return id

def insert_into_participacion(id_deportista, id_evento, id_equipo, edad, medalla, mySQL):
    if not mySQL:
        sql = ("INSERT INTO Participacion (`id_deportista`, `id_evento`, `id_equipo`, `edad`, `medalla`) "
            "VALUES (?, ?, ?, ?, ?)")
    else:
        sql = ("INSERT INTO Participacion (`id_deportista`, `id_evento`, `id_equipo`, `edad`, `medalla`) "
            "VALUES (%s, %s, %s, %s, %s)")
    values = (id_deportista, id_evento, id_equipo, edad, medalla)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

def insert_into_evento(evento, id_olimpiada, id_deporte, mySQL):
    if not mySQL:
        sql = "INSERT INTO Evento (`nombre`,`id_olimpiada`,`id_deporte`) VALUES (?, ?, ?)"
    else:
        sql = "INSERT INTO Evento (`nombre`,`id_olimpiada`,`id_deporte`) VALUES (%s, %s, %s)"
    values = (evento, id_olimpiada,  id_deporte)
    cur = conn.cursor()
    cur.execute(sql, values)
    id = cur.lastrowid
    conn.commit()
    return id

def insert_into_olimpiada(games, year, season, city, mySQL):
    if not mySQL:
        sql = "INSERT INTO Olimpiada (`nombre`,`anio`,`temporada`,`ciudad`) VALUES (?, ?, ?, ?)"
    else:
        sql = "INSERT INTO Olimpiada (`nombre`,`anio`,`temporada`,`ciudad`) VALUES (%s, %s, %s, %s)"
    values = (games, year, season, city)
    cur = conn.cursor()
    cur.execute(sql, values)
    id = cur.lastrowid
    conn.commit()
    return id

def crear_BBDD(mySql):
    path = input("Ruta del archivo csv para rellenar las tablas de ediciones olimpicas: ")
    try:
        with open(path) as csvFile:
            reader = csv.reader(csvFile)
            reader.__next__()
            mismo_athleta = -1
            for deportista in reader:
                if deportista[0] == "1000":
                    break
                print("Deportista -> ", deportista[0])
                if deportista[0] != mismo_athleta:
                    altura = deportista[4]
                    peso = deportista[5]
                    if deportista[4] == 'NA':
                        altura = 0
                    if deportista[5] == 'NA':
                        peso = 0
                    insert_into_deportista(deportista[0], deportista[1], deportista[2], peso, altura, mySql)
                    mismo_athleta = deportista[0]

                id_deporte = exist_deporte(deportista[12], mySql)
                if id_deporte == -1:
                    id_deporte = insert_into_deporte(deportista[12], mySql)

                id_equipo = exist_equipo(deportista[6], deportista[7], mySql)
                if id_equipo == -1:
                    id_equipo = insert_into_equipo(deportista[6], deportista[7], mySql)

                id_olimpiada = exist_olimpiadas(deportista[9], deportista[10], mySql)
                if id_olimpiada == -1:
                    id_olimpiada = insert_into_olimpiada(deportista[8], deportista[9], deportista[10], deportista[11], mySql)

                id_evento = exist_evento(deportista[13], id_deporte, id_olimpiada, mySql)
                if id_evento == -1:
                    id_evento = insert_into_evento(deportista[13], id_olimpiada, id_deporte, mySql)

                edad = deportista[3]
                if deportista[3] == 'NA':
                    edad = 0

                insert_into_participacion(deportista[0], id_evento, id_equipo, edad, deportista[14], mySql)
        conn.close()
        print("Se ha creado la BBDD correctamente.")
    except FileNotFoundError:
        print("El archivo csv no existe")


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
        with open("/home/dm2/PycharmProjects/pythonProject1/ediciones_olimpicas.sql", "r") as f:
            result_iterator = cursor.execute(f.read(), multi=True)
            dbConn.commit()
        cursor.close()
        dbConn.close()

        crear_BBDD(True)
    if resp == 2:
        conn = sqlite3.connect("/home/dm2/PycharmProjects/pythonProject1/ediciones_olimpicas.db")

        #Borrar contenido
        cursor = conn.cursor()
        with open("/home/dm2/PycharmProjects/pythonProject1/ediciones_olimpicas.db.sql", "r") as f:
            cursor.executescript(f.read())

        crear_BBDD(False)
    if resp == 3:
        bbddd = input("MySQL o SQLite: ").lower()
        if bbddd.__eq__("mysql"):
            mySQL = True
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        else:
            mySQL = False
            conn = sqlite3.connect("/home/dm2/PycharmProjects/pythonProject1/ediciones_olimpicas.db")
        lstDeportistas = self.__get_deportista_partipacion_diferentes_deportes()
        print("Datos deportistas: ")
        for deportista in lstDeportistas:
            participacion_olimpicas = self.__get_info_participaciones_olimpicas_deportista__(mySQL, deportista[0])
            print("Deportista:")
            print(deportista[1], deportista[2], deportista[3], deportista[4])
            print("Particiones Olimpicas:")
            for participacion in participacion_olimpicas:
                print(participacion[0], participacion[1], participacion[2], participacion[3], participacion[4],
                      participacion[5])
    if resp == 4:
        connSQL.listar_deportistas_que_participan(user, password, host, database)
    if resp == 5:
        connSQL.modificar_medalla_deportista(user, password, host, database)
    if resp == 6:
        connSQL.aniadir_deportista_participacion(user, password, host, database)
    if resp == 7:
        connSQL.eliminar_participacion(user, password, host, database)
