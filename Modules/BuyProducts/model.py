import pymysql
from Libs.db import Database

class Model():
    def __init__(self):
        
        self._conn, self._cursor = Database.get_connection()
        if not self._conn:
            print('Something went wrong (Error Code 30)')

    def buy_product(self, product_id, price):
        try:
            query = f'''UPDATE products SET product_quantity =  product_quantity-1
                        WHERE product_id = {product_id} AND product_quantity > 0'''
            result = self._cursor.execute(query)
            transaction_query = f'''INSERT INTO transaction (transaction_name, type, product_id, product_quantity, amount)
                                    VALUES('Buy Product', 'Buy', {product_id}, 1, {price})'''
            self._cursor.execute(transaction_query)
            self._conn.commit()
            return result
        except pymysql.DatabaseError as error:
            print(str(error))
            return False
        except AttributeError as error:
            print(str(error))
            return False

    def check_product_exist(self, product_id):
        try:
            query = f'''SELECT count(*) as count, product_price 
                        from products where product_id = {product_id}'''
            self._cursor.execute(query)
            result = self._cursor.fetchall()
            return result[0]['count'], result[0]['product_price']
        except pymysql.DatabaseError as error:
            print(str(error))
            return False, None
        except AttributeError as error:
            print(str(error))
            return False, None
