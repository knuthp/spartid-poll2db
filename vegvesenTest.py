import unittest
import vegvesen 



class MyTest(unittest.TestCase):
    def test(self):
        filename = "test/data/GetPredefinedTravelTimeLocations.xml"
#        filename = "test/data/locationsTmp.xml"
        with open (filename, "r") as myfile:
            data=myfile.read()
            location = vegvesen.Locations(data);
#            self.assertEqual(location.toJson(), "a")