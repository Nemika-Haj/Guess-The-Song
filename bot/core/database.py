from pymongo import MongoClient
from .files import Data
from .api import avatar

config = Data("config").yaml_read()

client = MongoClient(config["mongo-uri"])

class Levels:
    def __init__(self, user_id=None):
        self.levels = client["jam"]["levels"]
        self.user = user_id
        if user_id:
            if self.exists() == False:
                self.add_user

    def get_all(self):
        return self.levels.find({})

    @property
    def add_user(self):
        self.levels.insert_one({"_id":self.user, "xp":0, "level":0, "avatar":avatar(self.user)})

    def exists(self):
        return self.levels.find({'_id': self.user}).count() > 0
    
    def get(self):
        return self.levels.find_one({"_id": self.user})

    def add_xp(self, xp=1):
        self.levels.update_one({"_id": self.user}, {"$inc": {"xp": xp}, "$set": {"avatar": avatar(self.user)}})
        self.check_levelup()
    
    def add_level(self, level=1):
        self.levels.update_one({"_id": self.user}, {"$inc": {"level": level}})

    def remove_xp(self, xp=1):
        self.levels.update_one({"_id": self.user}, {"$inc": {"xp": -xp}})
    
    def remove_level(self, level=1):
        self.levels.update_one({"_id": self.user}, {"$inc": {"level": -level}})

    def set(self, **kwargs):
        self.levels.update_one({"_id": self.user}, {"$set": kwargs})

    def check_levelup(self):
        data = self.get()
        
        if data['xp'] >= data['level']*3:
            self.add_level()
            self.set(xp=0)
