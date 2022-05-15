import sqlite3, pandas

# adds csv to db, only needs to be run once


# create cursor
con = sqlite3.connect("static\shakespeare.db")
cur = con.cursor()

# pandas hack to not have to do headers myself
df = pandas.read_csv("static\Shakespeare_data.csv")

# some cleaning?
new = df["ActSceneLine"].str.split(".", expand=True)
df["Act"] = new[0]
df["Scene"] = new[1]
df["Line"] = new[2]
df = df.drop("ActSceneLine", 1)
# cleaning done

df.to_sql("shakespeare", con, if_exists="replace", index=False)

cur.execute("create virtual table playsearch using fts5(playsrowid,text)")

cur.execute("insert into playsearch select dataline, playerline from shakespeare")

# test select:
cur.execute(
    "select text,player, act, scene,  line, play from playsearch join shakespeare on playsearch.playsrowid = shakespeare.dataline where text match 'whether tis'"
)
print(cur.fetchall())

con.close()
