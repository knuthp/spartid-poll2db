import unittest
import vegvesen 



class LocationsTest(unittest.TestCase):
    data = ""
    
    def testPublicationTime(self):
            location = vegvesen.Locations(self.data);
            self.assertEquals(str(location.toJson()['publicationTime']), "2016-02-24 13:30:32+01:00")

    def testOneName(self):
            location = vegvesen.Locations(self.data);
            self.assertEquals(location.toJson()['predefinedLocations']['100249']['name'], "Lagunen - Birkelandskrysset")

    def testOneGeoLocations(self):
            location = vegvesen.Locations(self.data);
            self.assertEquals(location.toJson()['predefinedLocations']['100249']['geolocations']['utm33'][:2], [{'x' : -37016, 'y' : 6723367}, {'x' : -37000, 'y' : 6723366}])

    def testReadAllLocations(self):
            location = vegvesen.Locations(self.data);
            self.assertEquals(len(location.toJson()['predefinedLocations']), 156)

    def setUp(self):
        unittest.TestCase.setUp(self)
        filename = "tests/data/GetPredefinedTravelTimeLocations.xml"
        with open (filename, "r") as myfile:
            self.data=myfile.read()
        
