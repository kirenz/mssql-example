"""Example that connects to SQL Server and reads the SOPRA discount views."""

import os
import urllib.parse

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# --- CONFIGURATION SECTION ---

# Load variables defined in a .env file.
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

# Build the connection string. urllib.parse.quote_plus handles special characters.
params = urllib.parse.quote_plus(
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate={'Yes' if TRUST_CERT else 'No'};"
)

# create_engine builds a SQLAlchemy Engine object that manages the connection.
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


# --- SQL QUERY SECTION ---

DISCOUNT_QUERY = text(
    """
    SELECT TOP (5)
        RabattID,
        Kunde,
        MengeVon,
        MengeBis,
        RabattProzent,
        GiltVon,
        GiltBis
    FROM list_views.V_LIST_B2B_DISCOUNT
    ORDER BY RabattID DESC;
    """
)

CUSTOMER_QUERY = text(
    """
    SELECT TOP (5)
        CUSTOMER_ID,
        CUSTOMER_LONG
    FROM dbo.LOV_CUSTOMER
    ORDER BY CUSTOMER_ID;
    """
)


# --- EXECUTION SECTION ---

with engine.connect() as connection:
    # Run a quick check to confirm we can talk to the server.
    version = connection.execute(text("SELECT @@VERSION AS version;")).scalar()
    print("Connection successful!")
    print("SQL Server version:", version)

    # Pull the SOPRA discount overview into a pandas DataFrame.
    discounts = pd.read_sql(DISCOUNT_QUERY, connection)
    print("\nLatest discounts:")
    print(discounts.to_string(index=False))

    # Pull the customer list of values used by the Streamlit dropdown.
    customers = pd.read_sql(CUSTOMER_QUERY, connection)
    print("\nCustomer LOV sample:")
    print(customers.to_string(index=False))
