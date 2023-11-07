import ConexionSQL
import mysql.connector
import sqlite3
import csv

host = "localhost"
user = "admin"
password = "password"
database = "ediciones_olimpicas"

resp = -1

connSQL = ConexionSQL.Conexion()

while resp != 0:
    try:
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
            connSQL.crear_conexion_MySQL(user, password, host, database)
            connSQL.borrar_BBDD(True, user, password, host)
            connSQL.crear_BBDD(True)
        elif resp == 2:
            connSQL.crear_conexion_SQLite()
            connSQL.borrar_BBDD(False)
            connSQL.crear_BBDD(False)
        elif resp == 3:
            connSQL.listar_deporistas_participan_diferentes_deportes(user, password, host, database)
        elif resp == 4:
            connSQL.listar_deportistas_que_participan(user, password, host, database)
        elif resp == 5:
            connSQL.modificar_medalla_deportista(user, password, host, database)
        elif resp == 6:
            connSQL.aniadir_deportista_participacion(user, password, host, database)
        elif resp == 7:
            connSQL.eliminar_participacion(user, password, host, database)
