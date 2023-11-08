import sqlite3
import mysql.connector

class ConexionSQL:

    def mostrar_lista(self, cabezera, lista, info_user, strError, evento=False):
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


    def __insert_into_deportista2__(self, nombre, sexo, height, weight, mySQL):
        if not mySQL:
            sql = ("INSERT INTO Deportista (`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (?, ?, ?, ?)")
        else:
            sql = ("INSERT INTO Deportista (`Nombre`,`Sexo`,`Height`,`Weight`) VALUES (%s, %s, %s, %s)")
        values = (nombre, sexo, height, weight)
        cur = self.conn.cursor()
        cur.execute(sql, values)
        id = cur.lastrowid
        self.conn.commit()
        return id
