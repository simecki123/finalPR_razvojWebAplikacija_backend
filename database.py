from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
import models

# MongoDB configuration
MONGODB_URL = "*****************"  # Update with your MongoDB connection URL
DB_NAME = "**************"  # Update with your database name

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

    async def get_cars(self):
        collection = self.connector.get_collection("cars")
        cars = await collection.find().to_list(None)
        return [models.Cars(**car) for car in cars]

    async def get_users(self):
        collection = self.connector.get_collection("users")
        users = await collection.find().to_list(None)
        return [models.User(**user) for user in users]

    async def get_user_cars(self):
        collection = self.connector.get_collection("user_cars")
        user_cars = await collection.find().to_list(None)
        return [models.User_car(**uc) for uc in user_cars]

    async def add_car(self, car: models.Cars):
        collection = self.connector.get_collection("cars")
        await collection.insert_one(car.dict())

    async def add_user(self, user: models.User):
        collection = self.connector.get_collection("users")
        await collection.insert_one(user.dict())

    async def add_user_car(self, user_car: models.UserCar):
        collection = self.connector.get_collection("user_cars")
        await collection.insert_one(user_car.dict())

    async def delete_car(self, car_id: int):
        collection = self.connector.get_collection("cars")
        await collection.delete_one({"id": car_id})

    async def delete_user(self, user_id: int):
        collection = self.connector.get_collection("users")
        await collection.delete_one({"id": user_id})

    async def delete_user_car(self, user_car_id: int):
        collection = self.connector.get_collection("user_cars")
        await collection.delete_one({"id": user_car_id})

