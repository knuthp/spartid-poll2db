import pymongo
import os
import logging
from datetime import datetime
from datetime import timedelta
from dateutil import tz

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
    
    def getLastTravelTime(self):
	if self.db.vegvesen_traveltime.count() > 0:
        	return self.db.vegvesen_traveltime.find().sort("$natural", -1).limit(1)[0]        
	else:
		return None
        
        
    def addLocationsIfNew(self, locations):
        if (self.db.vegvesen_locations.find({"publicationTime" : locations.getPublicationTime()}).count() == 0):
            objectId = self.db.vegvesen_locations.insert_one(locations.toJson())
            logging.info('Added new document for locations, objectId.inserted_id=%s', str(objectId.inserted_id))
            return objectId
        else:
            logging.info('Already existing location %s', locations.getPublicationTime())
            return False
    
    def getStats(self):
        return {'travelTime' : self.getStatsTravelTime(), 'locations' : self.getStatsLocations() }
    
    def getStatsTravelTime(self):
        collection = self.getDb().vegvesen_traveltime
        ret = {}
        ret['count'] = str(collection.count())
        lastItem = collection.find().sort("$natural", -1).limit(1)[0]
        ret['last'] = {'dateTime' : str(lastItem['publicationTime']),
                       'legCount' :  str(len(lastItem['legData']))}
        today = datetime.utcnow().date()
        yesterday = today - timedelta(1)
        start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
        yesterdayStart = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=tz.tzutc())
        ret['today'] = { 'count' : collection.find({"publicationTime" : { "$gte" : start} }).count() }
        ret['yesterday'] = { 'count' : collection.find({"publicationTime" : { "$gte" : yesterdayStart, "$lte" : start,} }).count() }
        return ret
    
    def getStatsLocations(self):
        collection = self.getDb().vegvesen_locations
        ret = {}
        ret['count'] = str(collection.count())
        lastItem = collection.find().sort("$natural", -1).limit(1)[0]
        ret['last'] = {'dateTime' : str(lastItem['publicationTime']),
                       'legCount' : str(len(lastItem['predefinedLocations'])) }
        return ret
