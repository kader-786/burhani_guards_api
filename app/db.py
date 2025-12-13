# app/db.py
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import get_pg_connection_string, PG_CONFIG
import logging

logger = logging.getLogger(__name__)

# Create a connection pool for better performance
connection_pool = None

def initialize_connection_pool(minconn=1, maxconn=10):
    """Initialize the PostgreSQL connection pool"""
    global connection_pool
    try:
        connection_pool = pool.SimpleConnectionPool(
            minconn,
            maxconn,
            get_pg_connection_string()
        )
        if connection_pool:
            logger.info("PostgreSQL connection pool created successfully")
    except Exception as e:
        logger.error(f"Error creating connection pool: {e}")
        raise

def get_connection_pool():
    """Get the connection pool, initialize if needed"""
    global connection_pool
    if connection_pool is None:
        initialize_connection_pool()
    return connection_pool

@contextmanager
def get_db_connection():
    """
    Get a connection from the pool using context manager
    Usage:
        with get_db_connection() as conn:
            # use connection
    """
    pool = get_connection_pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

def get_db_connection_direct():
    """
    Get a direct connection (not from pool)
    Useful for long-running operations
    """
    return psycopg2.connect(get_pg_connection_string())

def call_function(conn, function_name: str, params: dict = None):
    """
    Call a PostgreSQL function and return JSON result
    
    Args:
        conn: Database connection
        function_name: Full function name (e.g., 'bg.com_spr_login_json')
        params: Dictionary of parameters
    
    Returns:
        JSON result from the function
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Set search path to include the schema
            cursor.execute(f"SET search_path TO {PG_CONFIG['schema']}, public")
            
            # Build the function call
            if params:
                placeholders = ', '.join([f'%({key})s' for key in params.keys()])
                sql = f"SELECT * FROM {function_name}({placeholders})"
                cursor.execute(sql, params)
            else:
                sql = f"SELECT * FROM {function_name}()"
                cursor.execute(sql)
            
            # Fetch the result
            result = cursor.fetchone()
            
            # If the function returns a JSON column, extract it
            if result:
                # The function might return a single JSON column or multiple columns
                if len(result) == 1:
                    return list(result.values())[0]
                else:
                    return dict(result)
            
            return None
            
    except Exception as e:
        logger.error(f"Error calling function {function_name}: {e}")
        raise

def execute_query(conn, query: str, params: tuple = None):
    """
    Execute a query and return results as list of dictionaries
    
    Args:
        conn: Database connection
        query: SQL query
        params: Query parameters
    
    Returns:
        List of dictionaries
    """
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            
            # Check if there are results to fetch
            if cursor.description:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            
            return []
            
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise
