import sqlite3
import mysql.connector

class Conexion:

    def listar_deporistas_participan_diferentes_deportes(self, user, password, host, database):
        bbddd = input("MySQL o SQLite: ").lower()
        if bbddd.__eq__("mysql"):
            mySQL = True
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        else:
            mySQL = False
            conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
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


    def listar_deportistas_que_participan(self, user, password, host, database):
        bbddd = input("MySQL o SQLite: ").lower()
        if bbddd.__eq__("mysql"):
            mySQL = True
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        else:
            mySQL = False
            conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
        temporada = input("Winter o Summer (W/S): ").lower()
        if temporada.__eq__("w"):
            season = "Winter"
        else:
            season = "Summer"
        
        elementos = self.mostrar_olimpiada_deporte_evento(season, mySQL)
        evento = elementos[0]
        deporte = elementos[1]
        olimpiada = elementos[2]

        # Resumen
        deportistas = self.__get_deportistas_por_evento__(evento[0], mySQL)
        print("Informacion seleccionada:",olimpiada[3], olimpiada[2], deporte[1], evento[1])
        print("NOMBRE   SEXO    HEIGHT  WEIGHT  EQUIPO  MEDALLA")
        print("------------------------------------------------------------")
        for deportista in deportistas:
            print(deportista[1], deportista[2], deportista[3], deportista[9], deportista[12],deportista[8])

    def modificar_medalla_deportista(self, user, password, host, database):
        try:
            searchCaracter = input("Introduzca el texto para buscar deportistas:")
            conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
            lstDeportista = self.__get_deportista_for_search_characters__(searchCaracter)
            deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista, "Selecciona deportista(id): ", 
                "No se seleccionado ningun depostista de la lista")
            lstEventos = self.__get_evento_por_deportista__(deportista[0])
            evento = self.mostrar_lista("ID  EVENTO", lstEventos, "Selecciona evento(id): ", "No se seleccionado ningun evento de la lista")

            medalla = input("Introduzca el nuevo valor del campo medalla(NA/Bronce/Silver/Gold): ").capitalize()
            if(not medalla.__eq__("NA") and not medalla.__eq__("Bronce") and not medalla.__eq__("Silver") and not medalla.__eq__("Gold")):
                print("Valor no valido para el campo medalla")
                return
            
            if(self.__update_participacion_medalla__(deportista[0], evento[0], medalla, True)):
                print("Se a podido modificar el campo medalla en MySQL.")
            else:
                print("No se podido modificar el campo medalla en MySQL.")

            conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
            if(self.__update_participacion_medalla__(deportista[0], evento[0], medalla, False)):
                print("Se a podido modificar el campo medalla en SQLite.")
            else:
                print("No se podido modificar el campo medalla en SQLite.")

        except TypeError:
            print()

    def aniadir_deportista_participacion(self, user, password, host, database):
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
            deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista, "Selecciona deportista(id): ", 
                "No se seleccionado ningun depostista de la lista")
            if deportista is None:
                return
        temporada = input("Winter o Summer (W/S): ").lower()
        if temporada.__eq__("w"):
            season = "Winter"
        else:
            season = "Summer"
        elementos = self.mostrar_olimpiada_deporte_evento(season, True)
        evento = elementos[0]
        deporte = elementos[1]
        olimpiada = elementos[2]

        lstEquipo = self.__get_equipos__()
        equipo = self.mostrar_lista("ID  EQUIPO", lstEquipo, "Selecciona equipo(id): ", "No se seleccionado ningun depostista de la lista")

        medalla = input("Introduzca el nuevo valor del campo medalla(NA/Bronce/Silver/Gold): ").capitalize()
        if(not medalla.__eq__("NA") and not medalla.__eq__("Bronce") and not medalla.__eq__("Silver") and not medalla.__eq__("Gold")):
            print("Valor no valido para el campo medalla")
            return

        edad = int(input("la edad del deportista: "))

        self.__insert_into_participacion(deportista[0], evento[0], equipo[0], medalla, edad, True)
        conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
        self.__insert_into_participacion(deportista[0], evento[0], equipo[0], medalla, edad, False)

        print("Insertado la participacion en MySQL y SQLite.")
        print("Deportisa:", deportista[1], "Deporte:", deporte[1], "Olimpiada:", olimpiada[1], "Evento:", evento[1], "Medalla:", medalla)

    def eliminar_participacion(self, user, password, host, database):
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        searchCaracter = input("Introduzca el texto para buscar deportistas: ")
        lstDeportista = self.__get_deportista_for_search_characters__(searchCaracter)
        deportista = self.mostrar_lista("ID  NOMBRE  SEXO    HEIGHT  WEIGHT", lstDeportista, "Selecciona deportista(id): ", 
                "No se seleccionado ningun depostista de la lista")
        lstEventos = self.__get_evento_por_deportista__(deportista[0])
        evento = self.mostrar_lista("ID  EVENTO", lstEventos, "Selecciona evento(id): ", "No se seleccionado ningun evento de la lista")
        
        if(self.__delete_participacion__(deportista[0], evento[0], True)):
            print("Se a podido eliminar la participacion en MySQL.")
        else:
            print("No se podido eliminar la participacion en MySQL.")

        if(len(lstEventos) == 1):
            if(self.__delete_deportista__(deportista[0], True)):
                print("Se a podido eliminar el deportista en MySQL.")
            else:
                print("No se podido eliminar el deportista en MySQL.")

        conn = sqlite3.connect("../Datos_Olimpiadas/ediciones_olimpicas.db")
        if(self.__delete_participacion__(deportista[0], evento[0], False)):
            print("Se a podido eliminar la participacion en SQLite.")
        else:
            print("No se podido eliminar la participacion en SQLite.")

        if(len(lstEventos) == 1):
            if(self.__delete_deportista__(deportista[0], False)):
                print("Se a podido eliminar el deportista en SQLite.")
            else:
                print("No se podido eliminar el deportista en SQLite.")

    def mostrar_olimpiada_deporte_evento(self, season, mySQL):
        # Olimpiada
        olimpiadas = self.__get_olimpiadas_por_temporada__(season, mySQL)
        olimpiada = self.mostrar_lista("ID   GAME    YEAR    SEASON  CITY", olimpiadas, "Selecciona olimpiada(id): ",
                                            "No se a seleccionado ningun olimpiada de la lista.")
        # Deporte
        deportes = self.__get_deportes_por_olimpiada__(olimpiada[0], mySQL)
        deporte = self.mostrar_lista("ID   SPORT", deportes, "Selecciona deporte(id): ",
                                          "No se a seleccionado ningun deporte de la lista.")

        # Evento
        eventos = self.__get_eventos__(olimpiada[0], deporte[0], mySQL)
        evento = self.mostrar_lista("ID   EVENTO", eventos, "Selecciona evento(id): ",
                                         "No se a seleccionado ningun evento de la lista.", True)
        return evento, deporte, olimpiada

    def mostrar_lista(self, cabezera, lista, info_user, strError, evento = False):
        if len(lista) == 0:
            print("No se encontrado ningun resultado.")
            return None
        lstIDs = []
        print(cabezera)
        print("------------------------------------------------------------")
        for elemento in lista:
            lstIDs.append(elemento[0])
            if not evento:
                str = elemento.__str__().replace("(","").replace(",","").replace(")","").replace("'","")
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

    def insertar_evento(self, evento, id_deporte, id_olimpiada, mySQL):
        id = self.__exist_evento__(evento, id_deporte, id_olimpiada, mySQL)
        if id == -1:
           id = self.__insert_into_evento__(evento, id_deporte, id_olimpiada, mySQL)
        return id

    def insertar_olimpiada(self, games, year, season, city, mySQL):
        id = self.__exist_olimpiadas__(year, season, mySQL)
        if id == -1:
           id = self.__insert_into_olimpiada__(games, year, season, city, mySQL)
        return id

    def insertar_equipo(self, equipo, noc , mySQL):
        id = self.__exist_equipo__(equipo, noc, mySQL)
        if id == -1:
            id = self.__insert_into_equipo__(noc, equipo, mySQL)
        return id

    def insertar_deporte(self, deporte, mySQL):
        id = self.__exist_deporte__(deporte, mySQL)
        if id == -1:
            id = self.__insert_into_deporte__(deporte, mySQL)
        return id

    def __get_olimpiadas_por_temporada__(self, season, mySQL):
        if mySQL:
            sql = "SELECT * FROM Olimpiada WHERE season = %s"
        else:
            sql = "SELECT * FROM Olimpiada WHERE season = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (season,))
        return cur.fetchall()
    
    def __get_deportes_por_olimpiada__(self,id_olimpiada, mySQL):
        if mySQL:
            sql = ("SELECT * FROM deporte d WHERE EXISTS(SELECT * FROM evento e WHERE d.idDeporte = e.idDeporte AND EXISTS("
                   "SELECT * FROM olimpiada o WHERE e.idOlimpiada = o.idOlimpiada AND o.idOlimpiada = %s))")
        else:
            sql = ("SELECT * FROM deporte d WHERE EXISTS(SELECT * FROM evento e WHERE d.idDeporte = e.idDeporte AND EXISTS("
                   "SELECT * FROM olimpiada o WHERE e.idOlimpiada = o.idOlimpiada AND o.idOlimpiada = ?))")
        cur = self.conn.cursor()
        cur.execute(sql, (id_olimpiada,))
        return cur.fetchall()

    def __get_eventos__(self, id_olimpiada, id_deporte, mySQL):
        if mySQL:
            sql = "SELECT * FROM evento WHERE idOlimpiada = %s AND idDeporte = %s"
        else:
            sql = "SELECT * FROM evento WHERE idOlimpiada = ? AND idDeporte = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (id_olimpiada, id_deporte))
        return cur.fetchall()

    def __get_evento_por_deportista__(self, id_deportista):
        sql = "SELECT * FROM evento e WHERE EXISTS(SELECT * FROM participacion p WHERE e.idEvento = p.idEvento AND idDeportista = %s)"
        cur = self.conn.cursor()
        cur.execute(sql, (id_deportista, ))
        return cur.fetchall()

    def __get_deportistas_por_evento__(self, id_evento, mySQL):
        if mySQL:
            sql = ("SELECT * FROM deportista d, participacion p, equipo eq WHERE p.idDeportista = d.idDeportista AND eq.idEquipo = p.idEquipo AND EXISTS("
                   "SELECT * FROM evento e WHERE e.idEvento = p.idEvento AND p.idEvento = %s)")
        else:
            sql = ("SELECT * FROM deportista d, participacion p, equipo eq WHERE p.idDeportista = d.idDeportista AND eq.idEquipo = p.idEquipo AND EXISTS("
                   "SELECT * FROM evento e WHERE e.idEvento = p.idEvento AND p.idEvento = ?)")
        cur = self.conn.cursor()
        cur.execute(sql, (id_evento, ))
        return cur.fetchall()

    def __get_deportista_for_search_characters__(self, nombre ):
        sql = "SELECT * FROM deportista WHERE Nombre like(%s)"
        cur = self.conn.cursor()
        cur.execute(sql, ("%" + nombre + "%", ))
        return cur.fetchall()

    def __get_equipos__(self):
        sql = "SELECT * FROM equipo"
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def __get_info_participaciones_olimpicas_deportista__(self, mySQL, id_deportista):
        if not mySQL:
            sql = ("select Deporte, edad, evento, equipo, games, medalla from Participacion p, Equipo eq, Evento ev, "
                   "Olimpiada o, Deporte d where p.idEquipo = eq.idEquipo and ev.idEvento = p.idEvento and "
                   "ev.idOlimpiada = o.idOlimpiada and ev.idDeporte = d.idDeporte and p.idDeportista = ?")
        else:
            sql = ("select Deporte, edad, evento, equipo, games, medalla from Participacion p, Equipo eq, Evento ev, "
                   "Olimpiada o, Deporte d where p.idEquipo = eq.idEquipo and ev.idEvento = p.idEvento and "
                   "ev.idOlimpiada = o.idOlimpiada and ev.idDeporte = d.idDeporte and p.idDeportista = %s")
        cur = self.conn.cursor()
        cur.execute(sql, (id_deportista, ))
        return cur.fetchall()

    def __get_deportista_partipacion_diferentes_deportes(self):
        sql = ("select * from Deportista d where exists("
               "select * from Participacion p where d.idDeportista = p.idDeportista and exists("
               "select * from Evento e where p.idEvento = e.idEvento and exists("
               "select * from ediciones_olimpicas.Deporte d where d.idDeporte = e.idDeporte)))"
               "and 1 < ( select count(distinct(idDeporte)) from ediciones_olimpicas.Evento e2,"
               " ediciones_olimpicas.Participacion p2 where e2.idEvento = p2.idEvento "
               "and d.idDeportista = p2.idDeportista)order by d.idDeportista")
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def __update_participacion_medalla__(self, id_deportista, id_evento, medalla, mySQL):
        if mySQL:
            sql = "UPDATE participacion SET Medalla = %s WHERE idDeportista = %s AND idEvento = %s"
        else:
            sql = "UPDATE participacion SET Medalla = ? WHERE idDeportista = ? AND idEvento = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (medalla, id_deportista, id_evento))
        self.conn.commit()
        if(cur.rowcount != 0):
            return True
        return False

    def __delete_participacion__(self, id_deportista, id_evento, mySQL):
        if not mySQL:
            sql = "DELETE FROM participacion WHERE idDeportista = ? AND idEvento = ?"
        else:
            sql = "DELETE FROM participacion WHERE idDeportista = %s AND idEvento = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (id_deportista, id_evento))
        self.conn.commit()
        if(cur.rowcount != 0):
            return True
        return False

    def __delete_deportista__(self, id_deportista, mySQL):
        if not mySQL:
            sql = "DELETE FROM deportista WHERE idDeportista = ?"
        else:
            sql = "DELETE FROM deportista WHERE idDeportista = %s"
        cur = self.conn.cursor()
        cur.execute(sql, (id_deportista, ))
        self.conn.commit()
        if(cur.rowcount != 0):
            return True
        return False

    def __exist_evento__(self, evento, id_deporte, id_olimpiada, mySQL):
        if not mySQL:
            sql = "SELECT idEvento from Evento where Evento = ? AND idDeporte = ? AND idOlimpiada = ?"
        else:
            sql = "SELECT idEvento from Evento where Evento = %s AND idDeporte = %s AND idOlimpiada = %s"
        return self.__exist_element__(sql, (evento, id_deporte, id_olimpiada))

    def __exist_olimpiadas__(self, year, season, mySQL):
        if not mySQL:
            sql = "SELECT idOlimpiada from Olimpiada where year = ? AND season = ?"
        else:
            sql = "SELECT idOlimpiada from Olimpiada where year = %s AND season = %s"
        return self.__exist_element__(sql, (year, season))

    def __exist_equipo__(self, equipo, noc, mySQL):
        if not mySQL:
            sql = "SELECT idEquipo from Equipo where Equipo = ? AND NOC = ?"
        else:
            sql = "SELECT idEquipo from Equipo where Equipo = %s AND NOC = %s"
        return self.__exist_element__(sql, (equipo, noc))

    def __exist_deporte__(self, deporte, mySQL):
        if not mySQL:
            sql = "SELECT idDeporte from Deporte where Deporte = ?"
        else:
            sql = "SELECT idDeporte from Deporte where Deporte = %s"
        return self.__exist_element__(sql, (deporte, ))

    def __exist_element__(self, sql, values):
        cur = self.conn.cursor()
        cur.execute(sql, values)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        return -1

    def __insert_into_participacion(self, id_deportista, id_evento, id_equipo, medalla, edad, mySQL):
        if not mySQL:
            sql = ("INSERT INTO Participacion (`idDeportista`, `idEvento`, `idEquipo`, `Medalla`,`Edad`) "
                "VALUES (?, ?, ?, ?, ?)")
        else:
            sql = ("INSERT INTO Participacion (`idDeportista`, `idEvento`, `idEquipo`, `Medalla`,`Edad`) "
                "VALUES (%s, %s, %s, %s, %s)")
        values = (id_deportista, id_evento, id_equipo, medalla, edad)
        self.__insert_into__(sql, values)

    def __insert_into_evento__(self, evento, id_deporte, id_olimpiada, mySQL):
        if not mySQL:
            sql = "INSERT INTO Evento (`Evento`,`idDeporte`,`idOlimpiada`) VALUES (?, ?, ?)"
        else:
            sql = "INSERT INTO Evento (`Evento`,`idDeporte`,`idOlimpiada`) VALUES (%s, %s, %s)"
        values = (evento, id_deporte, id_olimpiada)
        return self.__insert_into__(sql, values)

    def __insert_into_olimpiada__(self, games, year, season, city, mySQL):
        if not mySQL:
            sql = "INSERT INTO Olimpiada (`games`,`year`, `season`,`city`) VALUES (?, ?, ?, ?)"
        else:
            sql = "INSERT INTO Olimpiada (`games`,`year`, `season`,`city`) VALUES (%s, %s, %s, %s)"
        values = (games, year, season, city)
        return self.__insert_into__(sql, values)

    def __insert_into_equipo__(self, noc, equipo, mySQL):
        if not mySQL:
            sql = "INSERT INTO Equipo (`NOC`, `Equipo`) VALUES (?, ?)"
        else:
            sql = "INSERT INTO Equipo (`NOC`, `Equipo`) VALUES (%s, %s)"
        values = (noc, equipo)
        return self.__insert_into__(sql, values)

    def __insert_into_deportista__(self, id, nombre, sexo, height, weight, mySQL):
        if not mySQL:
            sql = ("INSERT INTO Deportista (`idDeportista`,`Nombre`,`Sexo`,`Height`,`Weight`) VALUES ("
                "?, ?, ?, ?, ?)")
        else:
            sql = ("INSERT INTO Deportista (`idDeportista`,`Nombre`,`Sexo`,`Height`,`Weight`) VALUES ("
                "%s, %s, %s, %s, %s)")
        values = (str(id), nombre, sexo, str(height), str(weight))
        return self.__insert_into__(sql, values)

    def __insert_into_deportista2__(self, nombre, sexo, height, weight, mySQL):
        if not mySQL:
            sql = ("INSERT INTO Deportista (`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (?, ?, ?, ?)")
        else:
            sql = ("INSERT INTO Deportista (`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (%s, %s, %s, %s)")
        values = (nombre, sexo, height, weight)
        return self.__insert_into__(sql, values)

    def __insert_into_deporte__(self, deporte, mySQL):
        if not mySQL:
            sql = "INSERT INTO Deporte (`Deporte`) VALUES (?)"
        else:
            sql = "INSERT INTO Deporte (`Deporte`) VALUES (%s)"
        values = deporte
        return self.__insert_into__(sql, (values,))

    def __insert_into__(self, sql, values):
        cur = self.conn.cursor()
        cur.execute(sql, values)
        id = cur.lastrowid
        self.conn.commit()
        return id
