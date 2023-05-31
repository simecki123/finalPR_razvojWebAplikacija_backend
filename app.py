from fastapi import FastAPI
from database import Database
import models

app = FastAPI()
db = Database()

# First that will user see is list of all cars we have.
@app.get("/")
async def start_page():
    try:
        cars = await db.get_cars()
        return cars
    except Exception as e:
        return {"message": "Failed to retrieve cars from the database.", "error": str(e)}

# We want to search some special car
@app.get("/car/{mark}")
async def find_car_by_mark(mark: str):
    try:
        cars = await db.get_cars_by_mark(mark)
        return cars
    except Exception as e:
        return {"message": "Failed to retrive car with defined mark", "error": str(e)}

# Method that will allow user to reserve some availible car.
@app.get("/car_id/{id}")
async def find_car_by_ID_and_reserve(id: int):
    try:
        cars = await db.get_id_car_and_update(id)
        return cars
    except Exception as e:
        return {"message": "Failed to retrive car with specififc id", "error": str(e)}

# Method that adds new car to the database.
@app.post("/add_car")
async def add_car(car: models.Cars):
    try:
        await db.add_car(car)
        return {"message": "Car added successfully"}
    except Exception as e:
        return {"message": "Something went wrong while adding new car", "error": str(e)}

# Method that will delete selected car.   
@app.delete("/delete_car/{car_id}")
async def delete_car(car_id: int):
    try:
        await db.delete_car(car_id)
        return {"message": "Car deleted successfully"}
    except Exception as e:
        return {"message": "Something went wrong while deleting a new car", "error": str(e)}
    
