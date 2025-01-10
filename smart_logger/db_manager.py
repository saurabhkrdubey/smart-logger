import psycopg2
import psycopg2.pool 
import psycopg2.extras

from .constant import *




class DBManager:

    def __init__(self):

        self.pool = psycopg2.pool.SimpleConnectionPool(
            2, 10, 
            database = DATABASE, 
            user = USER, 
            host= HOST,
            password = PASSWORD,
            port = PORT
        )


    def get_cursor(self):
        self.ps_connection = self.pool.getconn()
        ps_cursor = self.ps_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return ps_cursor


    def insert(self, query):
        try:
            cursor = self.get_cursor()
            cursor.execute(
                query
            )
            self.ps_connection.commit()
            data = cursor.fetchone()
            return dict(data)
        except Exception as e:
            raise e
        finally:
            self.pool.putconn(self.ps_connection) 
            # if self.pool:
            #     self.pool.closeall()
        
    
    def fetchone(self, query):
        try:
            cursor = self.get_cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            return dict(data) if data else {}
        except Exception as e:
            raise e
        finally:
            self.pool.putconn(self.ps_connection) 
            # if self.pool:
            #     self.pool.closeall()
        




