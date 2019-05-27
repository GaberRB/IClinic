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


#insert dinamico
worksheet_list = wks.worksheets()
i = 0
while (len(worksheet_list) > i):
    rowinsert = []
    worksheet = wks.get_worksheet(i)
    table = (worksheet.title + '_sheet' + str(i))
    listaSheets = worksheet.get_all_values()
    col = listaSheets[0]
    del (listaSheets[0])
    insert_sql = 'insert into ' + table + ' (' + ','.join(col) + ') VALUES (' + ','.join(['%s'] * len(col)) + ')'
    for row in listaSheets:
        for field in row:
            if field == '':
                field = 'missing'
            elif type(field) != type('A'):
                field = str(field)
        rowinsert.append(tuple(row))
    print(insert_sql,',', rowinsert)
    cursor.executemany(insert_sql,rowinsert)
    cnx.commit()
    print('FOI INSERIDO :', cursor.rowcount , ' PARA A TABLE', table )
    i = i + 1
