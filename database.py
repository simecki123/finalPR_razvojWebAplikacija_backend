import bcrypt
from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
import models
from jose import jwt
from jose.exceptions import JWTError


# MongoDB configuration
MONGODB_URL = "mongodb+srv://sroncevic19:w4xw08PT1lpn2aXE@demo.zvdgd5c.mongodb.net/"  # Update with your MongoDB connection URL
DB_NAME = "Renta-car"  # Update with your database name

# Database connector
class DatabaseConnector:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DB_NAME]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

class Database:
    def __init__(self):
        self.connector = DatabaseConnector()

# This method gets all cars from database
    async def get_cars(self):
        collection = self.connector.get_collection("cars")
        cars = await collection.find().to_list(None)
        return [models.Cars(**car) for car in cars]

# This method gets all cars from database that has specific mark
    async def get_cars_by_mark(self, mark: str):
        collection = self.connector.get_collection("cars")
        cars = await collection.find({"mark": mark}).to_list(None)
        return [models.Cars(**car) for car in cars]
    
# This method gets car with specific id and simulates users choice of reserving that car
    async def get_id_car_and_update(self, car_id: int):
        collection = self.connector.get_collection("cars")
        car = await collection.find_one({"id": car_id})

        if car:
            if car["reserved"]:
                return "Car is already taken.", False
            else:
                await collection.update_one({"id": car_id}, {"$set": {"reserved": True}})
                return models.Cars(**car), True
        else:
            return HTTPException(status_code=404, detail="Car not found.")

# Database method that updates car to not be reserved
    async def get_car_and_return(self, car_id: int):
        collection = self.connector.get_collection("cars")
        car = await collection.find_one({"id": car_id})
        if car:
            if car["reserved"]:
                await collection.update_one({"id": car_id}, {"$set": {"reserved": False}})
                return models.Cars(**car), True
            else:
                return "Car is not reserved, cant return it", False
        else:
            return HTTPException(status_code=404, detail="Car not found.")

# This method will allow us to see all users in our database
    async def get_users(self):
        collection = self.connector.get_collection("users")
        users = await collection.find().to_list(None)
        return [models.User(**user) for user in users]
    
# Method for returning user by email
    async def get_user_by_email(self, email: str, password: str) -> Optional[models.User]:
        collection = self.connector.get_collection("users")
        user = await collection.find_one({"email": email})
        if user:
            user_obj = models.User(**user)
            if user_obj.verify_password(password):
                return user_obj
        return None

# Method that finds curently active user by email
    async def find_curent_user_by_email(self, email: str) -> Optional[models.User]:
        collection = self.connector.get_collection("users")
        user = await collection.find_one({"email": email})
        if user:
            user_obj = models.User(**user)
            return user_obj
        return None


# Method that finds relations between user and cars
    async def get_user_cars(self):
        collection = self.connector.get_collection("user_cars")
        user_cars = await collection.find().to_list(None)
        return [models.User_car(**uc) for uc in user_cars]

# This method will add a new car in database
    async def add_car(self, car: models.Cars):
        collection = self.connector.get_collection("cars")
        existing_car = await collection.find_one({"id": car.id})

        if existing_car:
            raise ValueError("Car with the same ID already exists")
    
        await collection.insert_one(car.dict())

# This method will allow us to create new user
    async def add_user(self, user: models.User):
        collection = self.connector.get_collection("users")
        existing_user = await collection.find_one({"email": user.email})

        if existing_user:
            raise ValueError("User with the same email already exists")

        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        user_dict = user.dict()
        user_dict["password"] = hashed_password.decode("utf-8")

        await collection.insert_one(user_dict)


# This method will add relation between user and the car
    async def add_user_car(self, user_car: models.UserCar):
        collection = self.connector.get_collection("user_cars")
        await collection.insert_one(user_car.dict())

# This method will delete selected car
    async def delete_car(self, car_id: int):
        collection = self.connector.get_collection("cars")
        await collection.delete_one({"id": car_id})

# This method will delete selected user
    async def delete_user(self, user_id: int):
        collection = self.connector.get_collection("users")
        await collection.delete_one({"id": user_id})

# This method will delete selected relation between user and car
    async def delete_user_car(self, user_id: int, car_id: int):
        collection = self.connector.get_collection("user_cars")
        await collection.delete_one({"id_user": user_id, "id_car": car_id})

# Method for admin to delete certain things
    async def admin_delete_user_car(self, car_id: int):
        collection = self.connector.get_collection("user_cars")
        await collection.delete_one({"id_car": car_id})

# Method for admin to delete certain things
    async def admin_delete_user_car_through_user(self, user_id: int):
        collection = self.connector.get_collection("user_cars")
        await collection.delete_one({"id_user": user_id})
