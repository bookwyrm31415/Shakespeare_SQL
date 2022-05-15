import sqlite3

con = sqlite3.connect("static\shakespeare.db")
cur = con.cursor()

cur.execute(
    "select text,player, act, scene,  line, play from playsearch join shakespeare on playsearch.playsrowid = shakespeare.dataline where text match 'whether tis'"
)
print(cur.fetchall())

con.close()
