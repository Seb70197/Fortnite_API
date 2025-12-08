from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, text
from app.config import settings
import urllib

#call the FastAPI constructor to create a new app instance
app = FastAPI()

API_KEY = settings.API_KEY
api_key_header = APIKeyHeader(name="x-api-key")

#defines the database connection parameters
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={settings.DB_SERVER};"
    f"DATABASE={settings.DB_NAME};"
    f"UID={settings.DB_USER};"
    f"PWD={settings.DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;")
#creates the SQLAlchemy engine using the connection parameters
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def verify_api_key(api_key: str = Depends(api_key_header)):

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

#define a root endpoint for health check
@app.get("/")
def health_check():
    return {"status": "API is running"}

#define an endpoint to get distinct player IDs and EPIC IDs
@app.get("/players", dependencies=[Depends(verify_api_key)])
def get_player_ids():
    try:
        with engine.connect() as conn:
            query = text("SELECT DISTINCT PLAYER_ID, EPIC_ID FROM fortnite_player")
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]
            
            return {"players": rows}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#define an endpoint to get player stats
@app.get("/stats", dependencies=[Depends(verify_api_key)])
def get_player_stats():
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM fortnite_player_stats")
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]
            
            return {"stats": rows}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#define an endpoint to get player stats history
@app.get("/stats_hist", dependencies=[Depends(verify_api_key)])
def get_player_stats_hist():
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM fortnite_player_stats_hist")
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]
            
            return {"stats": rows}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))