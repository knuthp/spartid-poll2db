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

print(doc['d2LogicalModel']['exchange']['supplierIdentification']['nationalIdentifier'])
print(doc['d2LogicalModel']['exchange'])

client = pymongo.MongoClient()
db = client.test_database
collection = db.test_collection
id = collection.insert_one(doc)
print(id)
