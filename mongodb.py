import pymongo
import os

class MongoPoll:
    client = {}
    db = {}
    def __init__(self):
        mongoUri = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
        print('Using mongodb url=%s', mongoUri)
        self.client = pymongo.MongoClient(mongoUri)
        self.db = self.client.get_default_database()
        
    def getDb(self):        
        return self.db 
    
    def addTravelTime(self, travelTime):
        objectId = self.db.vegvesen_traveltime.insert_one(travelTime)
        print('Added new document for traveltime, objectId.inserted_id=%s', str(objectId.inserted_id))
        return objectId
        