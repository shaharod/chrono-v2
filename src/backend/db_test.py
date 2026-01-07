import pyodbc
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env") 

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('DB_SERVER')};"
    f"DATABASE={os.getenv('DB_NAME')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print(f"✅ SUCCESS: Connected to {os.getenv('DB_NAME')}!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")