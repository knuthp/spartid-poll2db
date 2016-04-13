import os
import requests
import xmltodict
from dateutil import parser
import mongodb

class Vegvesen:
	username = ""
	password = ""
	
	def __init__(self):
		self.username = os.environ.get('VEGVESEN_USERNAME')
		self.password = os.environ.get('VEGVESEN_PASSWORD')
		
	def getTravelTime(self):
		url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/trafikkpublikasjon/reisetid/1/GetTravelTimeData'
		r = requests.get(url, auth=(self.username, self.password))
		return TravelTime(r.text)

class TravelTime:
	doc = {}
	def __init__(self, xml):
		self.doc = xmltodict.parse(xml)

	def toJson(self):
		payloadPublication = self.doc['d2LogicalModel']['payloadPublication']
		publicationTime = self.toDateTimeIso(payloadPublication['publicationTime'])

		data = {'publicationTime' : publicationTime,
			'publicationTimeSplit' : self.queryEnhanced(publicationTime),
			'publicationCreator' : payloadPublication['publicationCreator']['nationalIdentifier'],
			'legData' : self.extractElaboratedData(payloadPublication['elaboratedData'])
			}
		return data

	def extractElaboratedData(self, elaboratedData ):
		legsDict = {}
		for leg in elaboratedData:
			legData = self.extractBasicData(leg['basicData'])
			legsDict[legData['objectId']] = legData
			# print(legData)
	
		return legsDict
	
	def extractBasicData(self, basicData ):
		return { 'objectId' : basicData['pertinentLocation']['predefinedLocationReference']['@id'],
			 'travelTimeTrendType' : basicData.get('travelTimeTrendType'),
			 'travelTimeType' : basicData.get('travelTimeType'),
			 'travelTime' : basicData.get('travelTime', {}).get('duration'),
			 'freeFlowTravelTime' : basicData['freeFlowTravelTime']['duration'] }
	
	def toDateTimeIso(self, dateTimeString ):
		return parser.parse(dateTimeString)
	
	def queryEnhanced(self, dateTime ):
		return { 'year' : dateTime.year,
			 'month' : dateTime.month,
			 'day' : dateTime.day,
			 'dayOfWeek' : dateTime.isoweekday(),
			 'week' : dateTime.isocalendar()[1],
			 'hour' : dateTime.hour,
			 'min' : dateTime.minute,
			 'sec' : dateTime.second}


vegvesen = Vegvesen()
travelTime = vegvesen.getTravelTime()

mongodbPoll = mongodb.MongoPoll();
mongodbPoll.addTravelTime(travelTime.toJson())


