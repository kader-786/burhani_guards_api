# app/config.py
import os
from dotenv import load_dotenv

# Load .env file contents into environment variables
load_dotenv()

# PostgreSQL Configuration
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "127.0.0.1"),
    "port": os.getenv("PG_PORT", "5432"),
    "database": os.getenv("PG_DATABASE", "burhani_guards_db"),
    "user": os.getenv("PG_USER", "abdulkader"),
    "password": os.getenv("PG_PASSWORD", ""),
    "schema": os.getenv("PG_SCHEMA", "bg")
}

# API Configuration
API_BASE_PATH = os.getenv("API_BASE_PATH", "/BURHANI_GUARDS_API_TEST/api")

# Build connection string for psycopg2
def get_pg_connection_string():
    return f"host={PG_CONFIG['host']} port={PG_CONFIG['port']} dbname={PG_CONFIG['database']} user={PG_CONFIG['user']} password={PG_CONFIG['password']}"
