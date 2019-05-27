import mysql.connector
import json
cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost', database='IMPORT',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

cursor.execute("SELECT cast(a.id as UNSIGNED) id , a.nome, a.email," +
               "replace(replace(replace(a.telefone, '(', ''), ')', ''),'-', ''),a.valor, a.desconto," +
               " (cast(replace(a.valor, 'R$', '') as dec(12,2)) - (cast(a.desconto as dec(12,2))/100))  valor_com_desconto" +
               " FROM usuarios_sheet0 a")

usuarios_data = cursor.fetchall()
f = open("usuarios.txt", "w", newline="")
v = 'id; nome; email; telefone; valor_total; valor_com_desconto;'
f.write(v + '\n')

for x in usuarios_data:
    f.write(str(x).replace('Decimal', '')+ '\n')
f.close()




cursor.execute("SELECT a.id, a.user_id, b.nome dependente_de_id " +
                "FROM import.dependentes_sheet1 a " +
                "inner join usuarios_sheet0 b " +
                "on a.user_id = b.id ")
dependentes_data = cursor.fetchall()

f = open("dependentes.txt", "w", newline="")
d = 'id; usuarios_id; dependente_de_id;'
f.write(d + '\n')
for i in dependentes_data:
    f.write(str(i) + '\n')
f.close()





