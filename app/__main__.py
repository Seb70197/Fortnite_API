from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy import create_engine, text
from app.config import settings
from pydantic import BaseModel
import urllib
import bcrypt

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

class LoginRequest(BaseModel):
    user_id: str
    password: str

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
    
@app.put("/player_create", dependencies=[Depends(verify_api_key)])
def create_player(request: Request):
    try:
        player_data = request.json()
        player_id = player_data.get("PLAYER_ID")
        epic_id = player_data.get("EPIC_ID")
        
        if not player_id or not epic_id:
            raise HTTPException(status_code=400, detail="PLAYER_ID and EPIC_ID are required")
        
        with engine.connect() as conn:
            query = text("INSERT INTO fortnite_player (PLAYER_ID, EPIC_ID) VALUES (:player_id, :epic_id)")
            conn.execute(query, {"player_id": player_id, "epic_id": epic_id})
            conn.commit()
            
            return {"message": "Player created successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def hash_password(password: str) -> str:
    """encrypt the password entered by the user

    Args:
        password (str): The plain text password to be hashed

    Returns:
        str: The hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain text password against a hashed password

    Args:
        password (str): The plain text password to verify
        hashed (str): The hashed password to compare against

    Returns:
        bool: True if the password matches the hash, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.post("/login")
def login(data : LoginRequest):

    with engine.connect() as conn:
        query = text("SELECT password_hash FROM fortnite_player WHERE player_id = :uid")
        row = conn.execute(query, {"uid": data.user_id}).fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(data.password, row.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
    
    return {"message": "Login successful"}
    