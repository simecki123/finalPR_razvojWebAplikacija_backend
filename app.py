from fastapi import FastAPI
from database import Database
import models

app = FastAPI()
db = Database()
# Cars...................................................
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
        return {"message": "Something went wrong while deleting a car", "error": str(e)}
    
# Users.............................................................................................
# Method that will show us all users we have
@app.get("/Users")
async def start_page():
    try:
        users = await db.get_users
        return users
    except Exception as e:
        return {"message": "Failed to retrieve users from the database.", "error": str(e)}

# Method that will allow us to create new user
@app.post("/add_user")
async def add_user(user: models.User):
    try:
        await db.add_user(user)
        return {"message": "User added successfully"}
    except Exception as e:
        return {"message": "Something went wrong while adding a new user", "error": str(e)}


# Method that will allow us to delete some specific user.
@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    try:
        await db.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"message": "Something went wrong while deleting a User", "error": str(e)}
