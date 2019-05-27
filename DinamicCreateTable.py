import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector

cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost', database='IMPORT',
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key('1N6JFMIQR71HF5u5zkWthqbgpA8WYz_0ufDGadeJnhlo')


worksheet_list = wks.worksheets()
i = 0
#create table dinamic
while (len(worksheet_list) > i):
    worksheet = wks.get_worksheet(i)
    table = (worksheet.title + '_sheet' + str(i))
    columns = worksheet.row_values(1)
    createsqltable = """CREATE TABLE IF NOT EXISTS """ + table + " (" + " VARCHAR(250),".join(columns) + " VARCHAR(250))"
    print (createsqltable)
    cursor.execute(createsqltable)
    print ('Criado a table ', table)
    cnx.commit()
    i = i + 1
