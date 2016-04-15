import vegvesen
import mongodb
import logging

logging.getLogger().setLevel(logging.INFO)


vegvesen = vegvesen.Vegvesen()
mongodbPoll = mongodb.MongoPoll();

travelTime = vegvesen.getTravelTime()

lastItem = mongodbPoll.getLastTravelTime()
logging.info(travelTime.diff(lastItem))

mongodbPoll.addTravelTime(travelTime)

