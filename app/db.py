import os
from psycopg2 import pool
import psycopg2.extras

class DB:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_CONN_STRING")
        if not self.connection_string:
            raise SystemError("Database connection string not found")
        
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=self.connection_string
        )

    def execute_query(self, query, params=None, fetch=False):
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                conn.commit()
        finally:
            self.pool.putconn(conn)

    def close_all(self):
        self.pool.closeall()