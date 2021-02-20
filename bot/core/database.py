import pymongo as MongoClient
from .files import Data

config = Data("config").yaml_read()

client = MongoClient(config["mongo-uri"])

class Levels:
    def __init__(self, user_id):
        self.levels = client["main"]["levels"]
        self.user = user_id
        if exists() == False:
            add_user()

    @property
    def add_user(self):
        self.levels.insert_one({"_id":self.user, "xp":0, "level":0})

    def exists(self):
        return self.levels.find({'_id': self.user}).count() > 0
    
    def get(self):
        return self.levels.find_one({"_id": self.user})

    def add_xp(self, xp):
        self.levels.update_one({"_id": self.user}, {"$inc": {"xp": xp}})
    
    def add_level(self, level):
        self.levels.update_one({"_id": self.user}, {"$inc": {"level": level}})

    def remove_xp(self, xp):
        self.levels.update_one({"_id": self.user}, {"$inc": {"xp": -xp}})
    
    def remove_level(self, level):
        self.levels.update_one({"_id": self.user}, {"$inc": {"level": -level}})

    def set(self, **kwargs):
        self.levels.update_one({"_id": self.user}, kwargs)