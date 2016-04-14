import vegvesen
import mongodb
import logging

logging.getLogger().setLevel(logging.INFO)

vegvesen = vegvesen.Vegvesen()
mongodbPoll = mongodb.MongoPoll();

locations = vegvesen.getLocations()
mongodbPoll.addLocationsIfNew(locations)