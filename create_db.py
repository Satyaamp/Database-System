import sqlite3 as sql
con = sql.connect('db3.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS users")
sql ='''CREATE TABLE "users" (
	"UID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"UNAME"	TEXT,
	"UENNO"	TEXT,
    "UADD" TEXT,
    "UPIN" INTEGER
)'''
cur.execute(sql)
con.commit()
con.close()