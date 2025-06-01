import os
from psycopg2 import pool, DatabaseError, InterfaceError
import psycopg2.extras
from typing import Optional, List, Dict, Any

class DB:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_CONN_STRING")
        if not self.connection_string:
            raise ValueError("DATABASE_CONN_STRING environment variable not set")
        
        try:
            self.pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.connection_string
            )
            # Test connection immediately
            self._test_connection()
        except (DatabaseError, InterfaceError) as e:
            raise ConnectionError(f"Failed to initialize connection pool: {e}")

    def _test_connection(self):
        """Test if the connection pool works"""
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        finally:
            if conn:
                self.pool.putconn(conn)

    def execute_query(
        self,
        query: str,
        params: Optional[tuple | dict] = None,
        fetch: bool = False
    ) -> Optional[List[Dict[str, Any]]]:
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    result = cur.fetchall()
                conn.commit()  # Explicit commit
                return result if fetch else None
        except Exception:
            conn.rollback()  # Rollback on error
            raise
        finally:
            self.pool.putconn(conn)

    def close_all(self):
        """Close all connections in the pool"""
        if hasattr(self, 'pool') and self.pool:
            try:
                self.pool.closeall()
            except Exception as e:
                raise RuntimeError(f"Failed to close connection pool: {e}")