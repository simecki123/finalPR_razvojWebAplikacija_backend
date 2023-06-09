from typing import Optional
from fastapi import FastAPI, HTTPException
from database import Database
import models
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from security import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


app = FastAPI()
db = Database()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Security
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)  
    if not user:
        return {"message": "Invalid username or password"}
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

# Testing security
@app.get("/protected_route")
async def protected_route(current_user: Optional[models.User] = Depends(get_current_user)):
    if current_user:
        user = await current_user
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

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
async def all_users():
    try:
        users = await db.get_users()  # Add parentheses to call the method
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

@app.get("/get_user_by_mail/{mail}")
async def get_user_email(user_mail: str):
    try:
        user = await db.get_user_by_email(user_mail)
        return user
    except Exception as e:
        return {"message": "Failed to retrieve users from the database.", "error": str(e)}