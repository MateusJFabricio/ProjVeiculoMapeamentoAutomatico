import sqlite3

#conn = sqlite3.connect("banco.db")
conn = sqlite3.connect(":testando:")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

#sql = "CREATE TABLE USUARIO(nome varchar(50))"
#cursor.execute(sql)

#sql = "ALTER TABLE USUARIO ADD idade integer"
#cursor.execute(sql)

sql = "INSERT INTO USUARIO(nome, idade) VALUES('Isabela',23)"
cursor.execute(sql)

conn.commit()


sql = "SELECT * FROM usuario"

for row in cursor.execute(sql):
    #input("Digite")
    print type(row)
    print row.keys()
    print row['nome']
    print row['idade']


#conn.close()
   

