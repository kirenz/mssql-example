"""Example that connects to SQL Server and prints the first rows of a table."""
# Python imports
import os
import urllib.parse
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# --- CONFIGURATION SECTION  ---

# Load variables defined in a .env file 
load_dotenv()

# Pull individual settings from the environment. 
# These keys must exist in your .env file.
SERVER = os.getenv("MSSQL_SERVER")
DATABASE = os.getenv("MSSQL_DATABASE")
USERNAME = os.getenv("MSSQL_USERNAME")
PASSWORD = os.getenv("MSSQL_PASSWORD")
DRIVER = os.getenv("MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")
# The driver might use a self-signed certificate. TRUST_CERT lets you opt in.
TRUST_CERT = os.getenv("TRUST_SERVER_CERTIFICATE", "false").lower() == "true"

if not all([SERVER, DATABASE, USERNAME, PASSWORD]):
    raise RuntimeError("Missing database credentials. Check your .env file.")

# Build the connection string. urllib.parse.quote_plus handles special characters in the password.
params = urllib.parse.quote_plus(
    f"DRIVER={{{DRIVER}}};"  # keep curly braces around the driver name
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate={'Yes' if TRUST_CERT else 'No'};"
)

# create_engine builds a SQLAlchemy Engine object that manages the database connection.
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# --- SQL QUERY SECTION  ---

# Example SQL statement 
SAMPLE_QUERY = text(
    """
    SELECT TOP (3)
           ID_Product,
           Material_Description,
           Product_Category,
           Transfer_Price_EUR
    FROM dbo.Dim_Product
    ORDER BY ID_Product;
    """
)

# --- EXECUTION SECTION  ---

with engine.connect() as connection:
    # Run a quick check to confirm we can talk to the server
    version = connection.execute(text("SELECT @@VERSION AS version"))
    print("Connection successful!")
    print("SQL Server version:", version.scalar())

    # Pull the dataset into a pandas DataFrame
    df = pd.read_sql(SAMPLE_QUERY, connection)
    print("\n Data:")
    print(df)
