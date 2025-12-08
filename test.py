import urllib
from sqlalchemy import create_engine, text
from app.config import settings
import pandas as pd

# params = urllib.parse.quote_plus(
#     f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#     f"SERVER={settings.DB_SERVER};"
#     f"DATABASE={settings.DB_NAME};"
#     f"UID={settings.DB_USER};"
#     f"PWD={settings.DB_PASSWORD};"
#     f"Encrypt=yes;"
#     f"TrustServerCertificate=no;")

# engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# # print(pd.read_sql("SELECT TOP 5 * FROM fortnite_player", engine))

# #Test the connection (optional)
# with engine.connect() as conn:
#     query = text("SELECT TOP 5 * FROM fortnite_player")
#     result = conn.execute(query)
#     rows = [dict(row) for row in result]
#     print(rows)

import requests

url ="https://fortnite-tracker-api-gzhjcubqfeerghaa.canadacentral-01.azurewebsites.net/docs"

test = requests.get(url)
print(test.json())

