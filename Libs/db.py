'''
    Module for database connection
'''

import logging
import pymysql

class Database:
    _conn = None

    @staticmethod
    def get_connection():
        username = 'root'
        password = 'root'
        host = 'localhost'
        port = 3306
        database = 'vending_machine'
        # ping mysql for checking connection is still alive or not
        ping_status = Database._ping()

        if Database._conn is None or not ping_status:
            try:
                Database._conn = pymysql.connect(host=host, user=username,
                                      passwd=password, port=port, db=database,
                                      charset='utf8', use_unicode=True,
                                      connect_timeout=60, autocommit=False)
            except pymysql.DatabaseError as error:
                logging.exception(str(error))
                return (False, False)
        return (Database._conn, Database._conn.cursor(pymysql.cursors.DictCursor))

    @staticmethod
    def _ping():
        '''
            Method to check if connection is still alive or not
        '''
        try:
            if Database._conn is None:
                return False
            cursor = Database._conn.cursor()
            cursor.execute('SELECT 1;')
            return True
        except pymysql.DatabaseError as error:
            logging.exception(str(error))
            return False
