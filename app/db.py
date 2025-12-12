import pyodbc
import pytds as tds
from app.config import CONN_STRING, TDS_CONFIG
from contextlib import contextmanager

def get_db_connection():
    return pyodbc.connect(CONN_STRING)

@contextmanager
def get_tds_connection():
    conn = tds.connect(
        server=TDS_CONFIG["server"],
        database=TDS_CONFIG["database"],
        user=TDS_CONFIG["user"],
        password=TDS_CONFIG["password"]
        # tds_version=7.1
        # as_dict=True
    )
    try:
        yield conn
    finally:
        conn.close()