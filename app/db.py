import os
import psycopg2

class DB:
    def __init__(self):
        self.connection_string = os.getenv("DATABSE_CONN_STRING")
        self.conn = None
        self.cur = None

        if self.connection_string is None:
            raise SystemError("Databse connection string not found")
        
    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.connection_string)

    def close(self):
        if self.cur:
            self.cur.close()

        if self.conn:
            self.conn.close()

    def select_query(self, query):
        if self.conn is None:
            return
        
        if self.cur is None:
            self.cur = self.conn.cursor()

        self.cur.execute(query)
        return self.cur.fetchall()
    
    def update_query(self, query):
        if self.conn is None:
            return
        
        if self.cur is None:
            self.cur = self.conn.cursor()

        self.cur.execute(query)
        self.conn.commit()
        
        
    
        


        

    
