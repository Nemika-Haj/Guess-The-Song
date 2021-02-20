import pymongo as MongoClient
from .files import Data

config = Data("config").yaml_read()

client = MongoClient(config["mongo-uri"])

class Levels:
    def __init__(self):
        self.levels = client["main"]["levels"]
    
    def add_user(self, user_id):
        self.levels.insert_one({"_id":user_id, "xp":0, "level":0})
    
    def get(self, user_id):
        self.levels.find_one({"_id": user_id})

    def add_xp(self, user_id, xp):
        self.levels.update_one({"_id": user_id}, {"$inc": {"xp": xp}})
    
    def add_level(self, user_id, level):
        self.levels.update_one({"_id": user_id}, {"$inc": {"level": level}})

    def remove_xp(self, user_id, xp):
        self.levels.update_one({"_id": user_id}, {"$inc": {"xp": -xp}})
    
    def remove_level(self, user_id, level):
        self.levels.update_one({"_id": user_id}, {"$inc": {"level": -level}})

    def set(self, user_id, **kwargs):
        self.levels.update_one({"_id": user_id}, kwargs)