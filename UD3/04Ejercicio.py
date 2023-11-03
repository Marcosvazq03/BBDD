import csv

import mysql.connector

conn = mysql.connector.connect(user="admin", password="password", host="localhost", database="ediciones_olimpicas")

def introducirDeportista(idDeportista, nombre, sex, alt, peso):
    sql = "INSERT INTO ediciones_olimpicas.Deportista VALUES(%s, %s, %s, %s, %s);"
    cur.execute(sql, (idDeportista, nombre, sex, alt, peso))

def introducirEquipo(idEquipo, nombre, noc):
    cur.execute("INSERT INTO Equipo VALUES(%s, %s, %s);", (idEquipo, nombre, noc))

def introducirEvento(idEvento, nombre, id_olim, id_dep):
    cur.execute("INSERT INTO Evento VALUES(%s, %s, %s, %s);", (idEvento, nombre, id_olim, id_dep))

def introducirParticipacion(idDep, idEv, idEq, edad, medalla):
    cur.execute("INSERT INTO ediciones_olimpicas.Participacion VALUES("+idDep+", "+idEv+", "+idEq+", "
                +edad+", '"+medalla+"');")

def introducirDeporte(idDeporte, nombre):
    cur.execute("INSERT INTO ediciones_olimpicas.Deporte VALUES("+idDeporte+", '"+nombre+"');")

def introducirOlimpiada(idOlimpiada, games, year, season, city):
    cur.execute("INSERT INTO Olimpiada VALUES(%s, %s, %s, %s, %s);", (idOlimpiada, games, year, season, city))


resp = -1
while not resp == 4:
    resp = int(input("""
    ¿Que desea hacer?
            1. Crear BBDD Mysql de olimpiadas
            2. Crear un fichero XML de deportistas
            3. Listado de olimpiadas
            4. Salir
    """))
    if resp == 1:
        cur = conn.cursor()
        listaP = []
        listaD = []
        listaE = []
        listaG = []
        idD = 0
        idE = 0
        idO = 0
        idEv = 0
        with open("/home/dm2/PycharmProjects/pythonProject1/csv/athlete_events.csv") as csvF:
            reader = csv.reader(csvF)
            reader.__next__()
            for r in reader:
                estaEvento = False
                estaParticipacion = False
                if r[0] not in listaP:
                    if r[0] == "1000":
                        break
                    idP = r[0]
                    print(idP)
                    nombre = r[1]
                    sexo = r[2]
                    altura = r[4]
                    if altura == "NA":
                        altura = 0
                    peso = r[5]
                    if peso == "NA":
                        peso = 0
                    introducirDeportista(str(idP), nombre, sexo, str(altura), str(peso))
                    listaP.append(r[0])
                    conn.commit()
                if r[12] not in listaD:
                    idD = idD+1
                    deporte = r[12]
                    introducirDeporte(str(idD), deporte)
                    listaD.append(r[12])
                    conn.commit()
                if r[6] not in listaE:
                    idE = idE+1
                    noc = r[7]
                    equipo = r[6]
                    introducirEquipo(str(idE), equipo, noc)
                    listaE.append(equipo)
                    conn.commit()
                if r[8] not in listaG:
                    idO = idO+1
                    games = r[8]
                    year = r[9]
                    season = r[10]
                    city = r[11]
                    introducirOlimpiada(str(idO), games, year, season, city)
                    listaG.append(r[8])
                    conn.commit()
                cur.close()

                # Insertar en Evento
                cur = conn.cursor(buffered=True)

                cur.execute("SELECT id_olimpiada from ediciones_olimpicas.Olimpiada WHERE nombre = '" + r[8] + "'")
                idOlimpiada = cur.fetchone()[0]

                cur.execute("SELECT id_deporte from ediciones_olimpicas.Deporte WHERE nombre = '" + r[12] + "'")
                idDeporte = cur.fetchone()[0]

                cur.execute("SELECT count(*) from ediciones_olimpicas.Evento WHERE nombre = %s AND id_olimpiada = %s AND id_deporte = %s", (r[13], idOlimpiada, idDeporte))
                contE = cur.fetchone()[0]
                if contE > 0:
                    estaEvento = True
                cur.close()
                cur = conn.cursor()
                if idOlimpiada is not None and idDeporte is not None:
                    if estaEvento == False:
                        idEv = idEv+1
                        event = r[13]
                        introducirEvento(str(idEv), event, str(idOlimpiada), str(idDeporte))
                        conn.commit()

                #Insertar en Participacion
                cur = conn.cursor(buffered=True)

                cur.execute("SELECT id_evento from ediciones_olimpicas.Evento WHERE nombre = %s AND id_olimpiada = %s AND id_deporte = %s", (r[13], idOlimpiada, idDeporte))
                idEvento = cur.fetchone()[0]

                cur.execute("SELECT id_equipo from ediciones_olimpicas.Equipo WHERE nombre = %s", (r[6],))
                idEquipo = cur.fetchone()[0]

                cur.execute("SELECT count(*) from ediciones_olimpicas.Participacion WHERE id_deportista = %s AND id_evento = %s",(idP, idEvento))
                contP = cur.fetchone()[0]
                if contP > 0:
                    estaParticipacion = True
                cur.close()
                cur = conn.cursor()
                if idEvento is not None and idEquipo is not None:
                    if estaParticipacion == False:
                        edad = r[3]
                        medalla = r[14]
                        if edad == 'NA':
                            edad = 0
                        introducirParticipacion(str(idP), str(idEvento), str(idEquipo), str(edad), medalla)
                        conn.commit()

        cur.close()
        conn.close()
