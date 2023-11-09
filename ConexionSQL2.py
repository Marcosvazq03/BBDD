import sqlite3
import mysql.connector

class ConexionSQL:


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
