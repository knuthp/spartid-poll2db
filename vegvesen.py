import os
import requests
import xmltodict
from dateutil import parser

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
	
	def getLocations(self):
		url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/trafikkpublikasjon/reisetid/1/GetPredefinedTravelTimeLocations'
		r = requests.get(url, auth=(self.username, self.password))
		return Locations(r.text)


class Locations:
	doc = {}
	def __init__(self, xml):		
		self.doc = xmltodict.parse(xml)
		
	def toJson(self):
		payloadPublication = self.doc['d2LogicalModel']['payloadPublication']
		publicationTime = self.toDateTimeIso(payloadPublication['publicationTime'])

		data = {'publicationTime' : publicationTime,
			'predefinedLocations' : self.extractPredefinedLocations(payloadPublication['predefinedLocationContainer'])
			}
		return data
	
	
	
	def getPublicationTime(self):
		payloadPublication = self.doc['d2LogicalModel']['payloadPublication']
		return self.toDateTimeIso(payloadPublication['publicationTime'])
	
	def extractPredefinedLocations(self, predefinedLocationContainer):
		locationsDict = {}
		for location in predefinedLocationContainer:
			locationId = location['@id']
			locationName =  location['predefinedLocationName']['values']['value']['#text']
			utm33String = location['location']['linearExtension']['linearLineStringExtension']['gmlLineString']['coordinates']
			utm33List = [x.strip() for x in utm33String.split(',', )]
			utm33 = []
			for pos in utm33List:
				splitPos = pos.split()
				utm33.append({'x': int(splitPos[0]), 'y': int(splitPos[1])})
				
			locationsDict[locationId] = { 'name' : locationName,
										'geolocations' : {
														'utm33' : utm33 
														}		
 									}
		return locationsDict
	
	def toDateTimeIso(self, dateTimeString ):
		return parser.parse(dateTimeString)
		
	
class TravelTime:
	data = {}
	
	def __init__(self, xml):
		self.toDict(xml)

	def toDict(self, xml):
		doc = xmltodict.parse(xml)
		payloadPublication = doc['d2LogicalModel']['payloadPublication']
		publicationTime = self.toDateTimeIso(payloadPublication['publicationTime'])

		self.data = {'publicationTime' : publicationTime,
			'publicationTimeSplit' : self.queryEnhanced(publicationTime),
			'publicationCreator' : payloadPublication['publicationCreator']['nationalIdentifier'],
			'legData' : self.extractElaboratedData(payloadPublication['elaboratedData'])
			}
	
	def toJson(self):
		return self.data

	def extractElaboratedData(self, elaboratedData ):
		legsDict = {}
		for leg in elaboratedData:
			legData = self.extractBasicData(leg['basicData'])
			legsDict[legData['id']] = legData
	
		return legsDict
	
	def extractBasicData(self, basicData ):
		return { 'id' : basicData['pertinentLocation']['predefinedLocationReference']['@id'],
			 'travelTimeTrendType' : basicData.get('travelTimeTrendType'),
			 'travelTimeType' : basicData.get('travelTimeType'),
			 'travelTime' : basicData.get('travelTime', {}).get('duration'),
			 'freeFlowTravelTime' : basicData['freeFlowTravelTime']['duration'] }

	def updateLegData(self, legId, legData):
		leg = self.data['legData'][legId]
		leg['travelTime'] = legData['travelTime']

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

	
	def diff(self, oldTravelTime2):
		diff = []
		for leg in self.data['legData']:
			new = self.data['legData'][leg]
			old = oldTravelTime2['legData'][leg]
			if new != old :
				diff.append({'id' : leg, 'old' : old, 'new' : new})
		return diff
	
	

