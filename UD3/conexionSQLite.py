from sqlite3 import connect
import csv

conn = connect("pokemon.db")
cur = conn.cursor()
with open("pokemon.sql") as f:
    cur.execute(f.read())
sql = "INSERT INTO pokemon values (?,?,?)"
poks = {}
with open("pokemon.csv") as f:
    reader = csv.DictReader(f)
    for r in reader:
        if r["ID_poke"] not in poks.keys():
            poks[r["ID_poke"]] = [r["ID_poke"], r["nom_ing"], r["tipo_1"]]
cur.executemany(sql, poks.values())
conn.commit()
cur.close()
conn.close()
