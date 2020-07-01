import pymysql
from Libs.db import Database

class Model():
    def __init__(self):
        
        self._conn, self._cursor = Database.get_connection()
        if not self._conn:
            print('Something went wrong (Error Code 30)')

    def get_products(self):
        try:
            query = 'SELECT * from products'
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            return True, result
        except pymysql.DatabaseError as error:
            print(str(error))
            return False
        except AttributeError as error:
            print(str(error))
            return False

    def check_product_exist(self, product_id):
        try:
            query = f'SELECT count(*) as count from products where product_id = {product_id}'
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            return result[0]['count']
        except pymysql.DatabaseError as error:
            print(str(error))
            return False
        except AttributeError as error:
            print(str(error))
            return False
            
    def update_product_stock(self, data):
        try:
            query = f'''UPDATE products SET product_quantity = {data['product_quantity']} 
                        where product_id = {data['product_id']}'''
            self._cursor.execute(query)

            transaction_query = f'''INSERT INTO transaction (transaction_name, type, product_id, product_quantity)
                                    VALUES('Reload Stock', 'Reload', {data['product_id']}, {data['product_quantity']})'''
            self._cursor.execute(transaction_query)
            self._conn.commit()
            return True
        except pymysql.DatabaseError as error:
            print(str(error))
            return False
        except AttributeError as error:
            print(str(error))
            return False
