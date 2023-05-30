from fastapi import FastAPI
from database import Database

app = FastAPI()
db = Database()

@app.get("/")
async def check_database_connection():
    try:
        await db.connector.client.admin.command("ping")
        return {"message": "Successfully connected to the database!"}
    except Exception as e:
        return {"message": "Failed to connect to the database.", "error": str(e)}
