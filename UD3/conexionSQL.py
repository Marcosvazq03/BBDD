import csv

import mysql.connector

conn = mysql.connector.connect(user="admin", password="password", hosts="localhost", database="olimpiadas")
sql = "select * from Deporte"
cur = conn.cursor()
cur.execute(sql)
print(cur)
print(cur.fetchall())

with open("pokemon.sql") as f:
    # cur.execute(f.read(), multi=True)
    cur.execute(f.read())

sql = "insert into pokemon values(12,'Pokemon','agua')"
cur.execute(sql)

lista = []
with open("pokemon.csv") as csvF:
    reader = csv.reader(csvF)
    reader.__next__()
    for r in reader:
        if r[0] not in lista:
            cur.execute(sql, (r[0], r[1], r[3]))
            lista.append(r[0])

conn.commit()
conn.close()
