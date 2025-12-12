# config.py
import os
from dotenv import load_dotenv

# Load .env file contents into environment variables
load_dotenv()

# Now fetch the connection string
CONN_STRING = os.getenv("CONN_STRING")

# For pytds
TDS_CONFIG = {
    "server": os.getenv("TDS_SERVER"),
    "database": os.getenv("TDS_DATABASE"),
    "user": os.getenv("TDS_USER"),
    "password": os.getenv("TDS_PASSWORD"),
}
