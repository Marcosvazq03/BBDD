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

def mostrar_lista(cabezera, lista, info_user, strError, evento=False):
    if len(lista) == 0:
        print("No se encontrado ningun resultado.")
        return None
    lstIDs = []
    print(cabezera)
    print("------------------------------------------------------------")
    for elemento in lista:
        lstIDs.append(elemento[0])
        if not evento:
            str = elemento.__str__().replace("(", "").replace(",", "").replace(")", "").replace("'", "")
            print(str)
        else:
            print(elemento[0], elemento[1])
    id = int(input(info_user))
    if not lstIDs.__contains__(id):
        print(strError)
        return None
    for elemento in lista:
        if id == elemento[0]:
            return elemento
    return None

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

        sql = ("select * from Deportista d where exists("
               "select * from Participacion p where d.id_deportista = p.id_deportista and exists("
               "select * from Evento e where p.id_evento = e.id_evento and exists("
               "select * from ediciones_olimpicas.Deporte de where de.id_deporte = e.id_deporte)))"
               "and 1 < ( select count(distinct(id_deporte)) from ediciones_olimpicas.Evento e2,"
               " ediciones_olimpicas.Participacion p2 where e2.id_evento = p2.id_evento "
               "and d.id_deportista = p2.id_deportista)order by d.id_deportista")
        cur = self.conn.cursor()
        cur.execute(sql)
        lstDeportistas = cur.fetchall()

        print("Datos deportistas: ")
        for deportista in lstDeportistas:
            if not mySQL:
                sql = (
                    "select nombre, edad, evento, equipo, games, medalla from Participacion p, Equipo eq, Evento ev, "
                    "Olimpiada o, Deporte d where p.id_equipo = eq.id_equipo and ev.id_evento = p.id_evento and "
                    "ev.id_olimpiada = o.id_olimpiada and ev.id_deporte = d.id_deporte and p.id_deportista = ?")
            else:
                sql = (
                    "select nombre, edad, evento, equipo, games, medalla from Participacion p, Equipo eq, Evento ev, "
                    "Olimpiada o, Deporte d where p.id_equipo = eq.id_equipo and ev.id_evento = p.id_evento and "
                    "ev.id_olimpiada = o.id_olimpiada and ev.id_deporte = d.id_deporte and p.id_deportista = %s")
            cur = self.conn.cursor()
            cur.execute(sql, (deportista[0],))
            participacion_olimpicas = cur.fetchall()

            print("Deportista:")
            print(deportista[1], deportista[2], deportista[3], deportista[4])
            print("Particiones Olimpicas:")
            for participacion in participacion_olimpicas:
                print(participacion[0], participacion[1], participacion[2], participacion[3], participacion[4],
                      participacion[5])
    if resp == 4:
        bbddd = input("MySQL o SQLite: ").lower()
        if bbddd.__eq__("mysql"):
            mySQL = True
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        else:
            mySQL = False
            conn = sqlite3.connect("/home/dm2/PycharmProjects/pythonProject1/ediciones_olimpicas.db")
        temporada = input("Winter o Summer (W/S): ").lower()
        if temporada.__eq__("w"):
            season = "Winter"
        else:
            season = "Summer"

        if mySQL:
            sql = "SELECT * FROM Olimpiada WHERE temporada = %s"
        else:
            sql = "SELECT * FROM Olimpiada WHERE temporada = ?"
        cur = conn.cursor()
        cur.execute(sql, (season,))
        olimpiadas = cur.fetchall()
        olimpiada = mostrar_lista("ID   GAME    YEAR    SEASON   CITY", olimpiadas, "Selecciona olimpiada(id): ", "No se ha seleccionado ningun olimpiada de la lista.")
        deportes = self.__get_deportes_por_olimpiada__(olimpiada[0], mySQL)
        deporte = mostrar_lista("ID   SPORT", deportes, "Selecciona deporte(id): ", "No se ha seleccionado ningun deporte de la lista.")
        eventos = self.__get_eventos__(olimpiada[0], deporte[0], mySQL)
        evento = mostrar_lista("ID   EVENTO", eventos, "Selecciona evento(id): ", "No se ha seleccionado ningun evento de la lista.", True)

        # Resumen
        deportistas = self.__get_deportistas_por_evento__(evento[0], mySQL)
        print("Informacion seleccionada:", olimpiada[3], olimpiada[2], deporte[1], evento[1])
        print("NOMBRE   SEXO    HEIGHT   WEIGHT   EQUIPO   MEDALLA")
        print("------------------------------------------------------------")
        for deportista in deportistas:
            print(deportista[1], deportista[2], deportista[3], deportista[9], deportista[12], deportista[8])
    if resp == 5:
        try:
            searchCaracter = input("Introduzca el texto para buscar deportistas:")
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
            lstDeportista = self.__get_deportista_for_search_characters__(searchCaracter)
            deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista,
                                            "Selecciona deportista(id): ",
                                            "No se seleccionado ningun depostista de la lista")
            lstEventos = self.__get_evento_por_deportista__(deportista[0])
            evento = self.mostrar_lista("ID  EVENTO", lstEventos, "Selecciona evento(id): ",
                                        "No se seleccionado ningun evento de la lista")

            medalla = input("Introduzca el nuevo valor del campo medalla(NA/Bronce/Silver/Gold): ").capitalize()
            if (not medalla.__eq__("NA") and not medalla.__eq__("Bronce") and not medalla.__eq__(
                    "Silver") and not medalla.__eq__("Gold")):
                print("Valor no valido para el campo medalla")
                break

            if (self.__update_participacion_medalla__(deportista[0], evento[0], medalla, True)):
                print("Se a podido modificar el campo medalla en MySQL.")
            else:
                print("No se podido modificar el campo medalla en MySQL.")

            conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
            if (self.__update_participacion_medalla__(deportista[0], evento[0], medalla, False)):
                print("Se a podido modificar el campo medalla en SQLite.")
            else:
                print("No se podido modificar el campo medalla en SQLite.")

        except TypeError:
            print("Error")
    if resp == 6:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        searchCaracter = input("Introduzca el texto para buscar deportistas: ")
        lstDeportista = self.__get_deportista_for_search_characters__(searchCaracter)
        if len(lstDeportista) == 0:
            print("No existe ninguna busqueda con los caracteres pasado, se creara un deportista.")
            nombre = input("Nombre: ")
            sexo = input("Sexo(M/F): ")
            height = int(input("Altura: "))
            weight = int(input("Peso: "))
            id = self.__insert_into_deportista2__(nombre, sexo, height, weight, True)
            conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
            self.__insert_into_deportista__(id, nombre, sexo, height, weight, False)
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
            deportista = (id, nombre, sexo, height, weight)
        else:
            deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista,
                                            "Selecciona deportista(id): ",
                                            "No se seleccionado ningun depostista de la lista")
            if deportista is None:
                break
        temporada = input("Winter o Summer (W/S): ").lower()
        if temporada.__eq__("w"):
            season = "Winter"
        else:
            season = "Summer"

        olimpiadas = self.__get_olimpiadas_por_temporada__(season, True)
        olimpiada = self.mostrar_lista("ID   GAME    YEAR    SEASON  CITY", olimpiadas,
                                       "Selecciona olimpiada(id): ",
                                       "No se ha seleccionado ningun olimpiada de la lista.")
        deportes = self.__get_deportes_por_olimpiada__(olimpiada[0], True)
        deporte = self.mostrar_lista("ID   SPORT", deportes, "Selecciona deporte(id): ",
                                     "No se ha seleccionado ningun deporte de la lista.")
        eventos = self.__get_eventos__(olimpiada[0], deporte[0], True)
        evento = self.mostrar_lista("ID   EVENTO", eventos, "Selecciona evento(id): ",
                                    "No se ha seleccionado ningun evento de la lista.", True)

        lstEquipo = self.__get_equipos__()
        equipo = self.mostrar_lista("ID  EQUIPO", lstEquipo, "Selecciona equipo(id): ",
                                    "No se seleccionado ningun depostista de la lista")

        medalla = input("Introduzca el nuevo valor del campo medalla(NA/Bronce/Silver/Gold): ").capitalize()
        if (not medalla.__eq__("NA") and not medalla.__eq__("Bronce") and not medalla.__eq__(
                "Silver") and not medalla.__eq__("Gold")):
            print("Valor no valido para el campo medalla")
            break

        edad = int(input("la edad del deportista: "))

        self.__insert_into_participacion(deportista[0], evento[0], equipo[0], medalla, edad, True)
        conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
        self.__insert_into_participacion(deportista[0], evento[0], equipo[0], medalla, edad, False)

        print("Insertado la participacion en MySQL y SQLite.")
        print("Deportisa:", deportista[1], "Deporte:", deporte[1], "Olimpiada:", olimpiada[1], "Evento:", evento[1],
              "Medalla:", medalla)
    if resp == 7:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        searchCaracter = input("Introduzca el texto para buscar deportistas: ")
        lstDeportista = self.__get_deportista_for_search_characters__(searchCaracter)
        deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista,
                                        "Selecciona deportista(id): ",
                                        "No se seleccionado ningun depostista de la lista")
        lstEventos = self.__get_evento_por_deportista__(deportista[0])
        evento = self.mostrar_lista("ID  EVENTO", lstEventos, "Selecciona evento(id): ",
                                    "No se seleccionado ningun evento de la lista")

        if (self.__delete_participacion__(deportista[0], evento[0], True)):
            print("Se a podido eliminar la participacion en MySQL.")
        else:
            print("No se podido eliminar la participacion en MySQL.")

        if (len(lstEventos) == 1):
            if (self.__delete_deportista__(deportista[0], True)):
                print("Se a podido eliminar el deportista en MySQL.")
            else:
                print("No se podido eliminar el deportista en MySQL.")

        conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
        if (self.__delete_participacion__(deportista[0], evento[0], False)):
            print("Se a podido eliminar la participacion en SQLite.")
        else:
            print("No se podido eliminar la participacion en SQLite.")

        if (len(lstEventos) == 1):
            if (self.__delete_deportista__(deportista[0], False)):
                print("Se a podido eliminar el deportista en SQLite.")
            else:
                print("No se podido eliminar el deportista en SQLite.")
