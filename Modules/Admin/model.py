import pymysql
from Libs.db import Database

class Model():
    def __init__(self):
        
        self._conn, self._cursor = Database.get_connection()
        if not self._conn:
            print('Something went wrong (Error Code 30)')

    def collect_cash(self):
        try:
            query = f'''SELECT timestamp FROM transaction WHERE type = 'Withdraw'
                        ORDER BY timestamp DESC LIMIT 1'''
            self._cursor.execute(query)
            timestamp = self._cursor.fetchall()

            cash_query = f''' SELECT SUM(amount) as amount FROM transaction'''
            if timestamp:
                ts = timestamp[0]['timestamp']
                cash_query += f' WHERE timestamp > "{ts}"'
            
            self._cursor.execute(cash_query)
            result = self._cursor.fetchall()
            
            amount = int(result[0]['amount']) if result[0]['amount'] else 0
            transaction_query = f'INSERT INTO transaction (transaction_name, type, amount) VALUES ("Collect cash", "Withdraw", {amount})'
            self._cursor.execute(transaction_query)
            self._conn.commit()

            return True, result[0]['amount']
        except pymysql.DatabaseError as error:
            print(str(error))
            return False, None
        except AttributeError as error:
            print(str(error))
            return False, None
            
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
            
