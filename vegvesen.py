import os
import requests
import xmltodict
import pymongo

url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/trafikkpublikasjon/reisetid/1/GetTravelTimeData'
username = os.environ.get('VEGVESEN_USERNAME')
password = os.environ.get('VEGVESEN_PASSWORD')
r = requests.get(url, auth=(username, password))

xml = r.text

doc = xmltodict.parse(xml)

payloadPublication = doc['d2LogicalModel']['payloadPublication']

data = {'publicationTime' : payloadPublication['publicationTime'],
	'publicationCreator' : payloadPublication['publicationCreator']['nationalIdentifier'],
	'elaboratedData' : [ {'id' : payloadPublication['elaboratedData'][0]['basicData']['pertinentLocation']['predefinedLocationReference']['@id'] }]
}

client = pymongo.MongoClient()
db = client.test_database
collection = db.test_collection
id = collection.insert_one(data)
print(id)
print(collection.find_one({"_id": id.inserted_id}))
