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

    def testReadAllLocations(self):
            location = vegvesen.Locations(self.data);
            self.assertEquals(len(location.toJson()['predefinedLocations']), 156)

    def setUp(self):
        unittest.TestCase.setUp(self)
        filename = "test/data/GetPredefinedTravelTimeLocations.xml"
        with open (filename, "r") as myfile:
            self.data=myfile.read()
        