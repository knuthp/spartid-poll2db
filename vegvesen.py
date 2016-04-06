import os
import requests
import xmltodict
import pymongo
from dateutil import parser

def extractElaboratedData( elaboratedData ):
	""
	legsDict = {}
	for leg in elaboratedData:
		legData = extractBasicData(leg['basicData'])
		legsDict[legData['id']] = legData
		# print(legData)

	return legsDict

def extractBasicData( basicData ):
	""
	return { 'id' : basicData['pertinentLocation']['predefinedLocationReference']['@id'],
		 'travelTimeTrendType' : basicData.get('travelTimeTrendType'),
		 'travelTimeType' : basicData.get('travelTimeType'),
		 'travelTime' : basicData.get('travelTime', {}).get('duration'),
		 'freeFlowTravelTime' : basicData['freeFlowTravelTime']['duration'] }

def toDateTimeIso( dateTimeString ):
	""
	return parser.parse(dateTimeString)

def queryEnhanced( dateTime ):
	""
	return { 'year' : dateTime.year,
		 'month' : dateTime.month,
		 'day' : dateTime.day,
		 'dayOfWeek' : dateTime.isoweekday(),
		 'week' : dateTime.isocalendar()[1],
		 'hour' : dateTime.hour,
		 'min' : dateTime.minute,
		 'sec' : dateTime.second}


url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/trafikkpublikasjon/reisetid/1/GetTravelTimeData'
username = os.environ.get('VEGVESEN_USERNAME')
password = os.environ.get('VEGVESEN_PASSWORD')
r = requests.get(url, auth=(username, password))

xml = r.text

doc = xmltodict.parse(xml)

payloadPublication = doc['d2LogicalModel']['payloadPublication']
publicationTime = toDateTimeIso(payloadPublication['publicationTime'])

data = {'publicationTime' : publicationTime,
	'publicationTimeSplit' : queryEnhanced(publicationTime),
	'publicationCreator' : payloadPublication['publicationCreator']['nationalIdentifier'],
	'legData' : extractElaboratedData(payloadPublication['elaboratedData'])
}

mongoUri = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
print('Using mongodb url=%s', mongoUri)
client = pymongo.MongoClient(mongoUri)
db = client.get_default_database()
collection = db.vegvesen_traveltime
id = collection.insert_one(data)
print('Added new document for traveltime, id=%s', str(id.inserted_id))


