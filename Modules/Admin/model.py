import pymysql
from Libs.db import Database

class Model():
    def __init__(self):
        
        self._conn, self._cursor = Database.get_connection()
        if not self._conn:
            print('Something went wrong (Error Code 30)')

            
    def get_transactions(self):
        try:
            query = 'SELECT * from transaction order by timestamp desc'
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            return True, result
        except pymysql.DatabaseError as error:
            print(str(error))
            return False
        except AttributeError as error:
            print(str(error))
            return False
            
