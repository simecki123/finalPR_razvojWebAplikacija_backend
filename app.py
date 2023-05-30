from fastapi import FastAPI
from database import Database

app = FastAPI()
db = Database()

@app.get("/")
async def start_page():
    try:
        cars = await db.get_cars()
        return cars
    except Exception as e:
        return {"message": "Failed to retrieve cars from the database.", "error": str(e)}

