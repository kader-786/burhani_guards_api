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

# def call_function(conn, function_name: str, params: dict = None):
#     """
#     Call a PostgreSQL function and return JSON result
    
#     Args:
#         conn: Database connection
#         function_name: Full function name (e.g., 'bg.com_spr_login_json')
#         params: Dictionary of parameters
    
#     Returns:
#         JSON result from the function
#     """
#     try:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             # Set search path to include the schema
#             cursor.execute(f"SET search_path TO {PG_CONFIG['schema']}, public")
            
#             # Build the function call
#             if params:
#                 placeholders = ', '.join([f'%({key})s' for key in params.keys()])
#                 sql = f"SELECT * FROM {function_name}({placeholders})"
#                 cursor.execute(sql, params)
#             else:
#                 sql = f"SELECT * FROM {function_name}()"
#                 cursor.execute(sql)
            
#             # Fetch the result
#             result = cursor.fetchone()
            
#             # If the function returns a JSON column, extract it
#             if result:
#                 # The function might return a single JSON column or multiple columns
#                 if len(result) == 1:
#                     return list(result.values())[0]
#                 else:
#                     return dict(result)
            
#             return None
            
#     except Exception as e:
#         logger.error(f"Error calling function {function_name}: {e}")
#         raise

def call_function(conn, function_name: str, params: dict = None):
    """
    Call a PostgreSQL function and return result(s)
    
    Handles two types of PostgreSQL functions:
    1. Functions that return JSON - returns the parsed JSON
    2. Functions that return TABLE/SETOF - returns list of dicts
    
    Args:
        conn: Database connection
        function_name: Full function name (e.g., 'bg.com_spr_login_json')
        params: Dictionary of parameters
    
    Returns:
        - For JSON return type: Returns the JSON object/array
        - For TABLE return type: Returns list of dictionaries (one per row)
        - None if no results
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
            
            # ✅ FIXED: Fetch ALL results, not just one
            results = cursor.fetchall()
            
            if not results:
                return None
            
            # Determine what type of result we have
            # If function returns JSON (single column), extract it
            if len(cursor.description) == 1:
                # Function returns a single JSON column
                # If multiple rows, return list; if single row, return the JSON value
                if len(results) == 1:
                    # Single row with JSON column
                    return list(results[0].values())[0]
                else:
                    # Multiple rows with JSON column (rare, but handle it)
                    return [list(row.values())[0] for row in results]
            else:
                # Function returns TABLE with multiple columns
                # Return list of dictionaries
                return [dict(row) for row in results]
            
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
