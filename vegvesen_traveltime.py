import vegvesen
import mongodb
import logging

logging.getLogger().setLevel(logging.INFO)


vegvesen = vegvesen.Vegvesen()
mongodbPoll = mongodb.MongoPoll();

travelTime = vegvesen.getTravelTime()
mongodbPoll.addTravelTime(travelTime)
