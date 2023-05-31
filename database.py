from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
import models

# MongoDB configuration
MONGODB_URL = "*****************"  # Update with your MongoDB connection URL
DB_NAME = "****************"  # Update with your database name

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
                return "Car is already taken."
            else:
                await collection.update_one({"id": car_id}, {"$set": {"reserved": True}})
                return models.Cars(**car)
        else:
            return "Car not found."


# This method will allow us to see all users in our database
    async def get_users(self):
        collection = self.connector.get_collection("users")
        users = await collection.find().to_list(None)
        return [models.User(**user) for user in users]

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
        existing_user = await collection.find_one({"id": user.id})

        if existing_user:
            raise ValueError("User with the same ID already exists")

        await collection.insert_one(user.dict())

    async def add_user_car(self, user_car: models.UserCar):
        collection = self.connector.get_collection("user_cars")
        existing_user_car = await collection.find_one({"id": user_car.id})

        if existing_user_car:
            raise ValueError("User car with the same ID already exists")

        await collection.insert_one(user_car.dict())

# This method will delete selected car
    async def delete_car(self, car_id: int):
        collection = self.connector.get_collection("cars")
        await collection.delete_one({"id": car_id})

# This method will delete selected user
    async def delete_user(self, user_id: int):
        collection = self.connector.get_collection("users")
        await collection.delete_one({"id": user_id})

    async def delete_user_car(self, user_car_id: int):
        collection = self.connector.get_collection("user_cars")
        await collection.delete_one({"id": user_car_id})

