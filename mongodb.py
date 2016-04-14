import pymongo
import os
import logging

class MongoPoll:
    client = {}
    db = {}
    def __init__(self):
        mongoUri = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
        logging.info('Using mongodb url=%s', mongoUri)
        self.client = pymongo.MongoClient(mongoUri)
        self.db = self.client.get_default_database()
        
    def getDb(self):        
        return self.db 
    
    def addTravelTime(self, travelTime):
        objectId = self.db.vegvesen_traveltime.insert_one(travelTime.toJson())
        logging.info('Added new document for traveltime, objectId.inserted_id=%s', str(objectId.inserted_id))
        return objectId
        
    def addLocationsIfNew(self, locations):
        if (self.db.vegvesen_locations.find({"publicationTime" : locations.getPublicationTime()}).count() == 0):
            objectId = self.db.vegvesen_locations.insert_one(locations.toJson())
            logging.info('Added new document for locations, objectId.inserted_id=%s', str(objectId.inserted_id))
            return objectId
        else:
            logging.info('Already existing location %s', locations.getPublicationTime())
            return False