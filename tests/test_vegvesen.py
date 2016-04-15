import os

import unittest
import vegvesen 
import xmltodict
class LocationsTest(unittest.TestCase):
    data = ""
    
    def testPublicationTime(self):
            location = vegvesen.Locations(self.data)
            self.assertEquals(str(location.toJson()['publicationTime']), "2016-02-24 13:30:32+01:00")

    def testOneName(self):
            location = vegvesen.Locations(self.data)
            self.assertEquals(location.toJson()['predefinedLocations']['100249']['name'], "Lagunen - Birkelandskrysset")

    def testOneGeoLocations(self):
            location = vegvesen.Locations(self.data)
            self.assertEquals(location.toJson()['predefinedLocations']['100249']['geolocations']['utm33'][:2], [{'x' : -37016, 'y' : 6723367}, {'x' : -37000, 'y' : 6723366}])

    def testReadAllLocations(self):
            location = vegvesen.Locations(self.data)
            self.assertEquals(len(location.toJson()['predefinedLocations']), 156)

    def setUp(self):
        unittest.TestCase.setUp(self)
        path = os.path.dirname(__file__)
        filename = path + "/data/GetPredefinedTravelTimeLocations.xml"
        with open (filename, "r") as myfile:
            self.data=myfile.read()
        



class TravelTimeTest(unittest.TestCase):
    data = ""
    
    def testTravelTime(self):
        travelTime = vegvesen.TravelTime(self.data)
        self.assertEquals(len(travelTime.toJson()['legData']), 156)


    def testTravelTimeEquals(self):
        travelTime1 = vegvesen.TravelTime(self.data)
        travelTime2 = vegvesen.TravelTime(self.data)
        self.assertEquals(travelTime1.toJson(), travelTime2.toJson())
        
    def testDiffNone(self):
        travelTime1 = vegvesen.TravelTime(self.data)
        travelTime2 = vegvesen.TravelTime(self.data)
        self.assertEqual(len(travelTime1.diff(travelTime2.toJson())), 0)

    def testDiffOne(self):
        travelTime1 = vegvesen.TravelTime(self.data)
        travelTime1.updateLegData('100192', {'travelTime' : u'55'})
        travelTime2 = vegvesen.TravelTime(self.data)
        diff = travelTime1.diff(travelTime2.toJson())
        self.assertEqual(diff[0]['id'], '100192')
        self.assertEqual(diff[0]['old']['travelTime'], '573.0')
        self.assertEqual(diff[0]['new']['travelTime'], u'55')

    def testDiffTwo(self):
        travelTime1 = vegvesen.TravelTime(self.data)
        travelTime1.updateLegData('100192', {'travelTime' : u'55'})
        travelTime1.updateLegData('100193', {'travelTime' : u'66'})
        travelTime2 = vegvesen.TravelTime(self.data)
        self.assertItemsEqual(travelTime1.diff(travelTime2.toJson())[0]['id'], '100193')
        self.assertItemsEqual(travelTime1.diff(travelTime2.toJson())[1]['id'], '100192')

        
    def setUp(self):
        unittest.TestCase.setUp(self)
        path = os.path.dirname(__file__)
        filename = path + "/data/GetTravelTimeData.xml"
        with open (filename, "r") as myfile:
            self.data=myfile.read()
    