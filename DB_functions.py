import psycopg2

tablename = 'eureca."BotRoles"'
orders = 'eureca."orders"'


class Database:
    def __init__(self):
        # self.conn = psycopg2.connect(dbname='Evrika', user='postgres',
        #                    password='12345678', host='localhost')
        self.conn = psycopg2.connect(dbname='eureca', user='postgres',
                                     password='postgres', host='172.28.2.117')

        self.cursor = self.conn.cursor()

    # def DBConnect(self):

    def CheckID(self, userid):
        with self.conn:
            self.cursor.execute(f'SElECT * FROM {tablename} WHERE userid = {int(userid)}')
            return bool(len(self.cursor.fetchall()))

    def AddUser(self, userid):
        with self.conn:
            self.cursor.execute(f'INSERT INTO {tablename} (userid) VALUES ({int(userid)})')

    def FieldInput(self, userid, field, value):
        with self.conn:
            self.cursor.execute(f"UPDATE {tablename} SET {field} = '{str(value)}' WHERE userid = {userid}")

    def FieldDelete(self, userid):
        with self.conn:
            self.cursor.execute(f'DELETE FROM {tablename} WHERE userid = {userid}')

    def CheckAccess(self, userid, role):
        with self.conn:
            self.cursor.execute(f'SElECT {role} FROM {tablename} WHERE userid = {int(userid)}')
            return self.cursor.fetchone()[0]

    def GetRow(self, userid):
        with self.conn:
            self.cursor.execute(f'SElECT * FROM {tablename} WHERE userid = {int(userid)}')
            mystrlist = self.cursor.fetchone()
            mystring = f'Ваше ФИО: {mystrlist[1]}\nВаш номер: {mystrlist[2]}\nВаш ИНН: {mystrlist[6]}\nВаша организация: {mystrlist[7]}'
            return mystring

    def MakeOrder(self, userid, productid):
        with self.conn:
            self.cursor.execute(f"INSERT INTO {orders} (userid, productid) VALUES ({int(userid)}, '{productid}')")

    def OrderFieldInput(self, userid, field, value):
        with self.conn:
            self.cursor.execute(f"UPDATE {orders} SET {field} = '{str(value)}' WHERE userid = {userid}")
