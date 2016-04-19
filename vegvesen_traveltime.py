import vegvesen
import mongodb
import logging
import messaging

logging.getLogger().setLevel(logging.INFO)


vegvesen = vegvesen.Vegvesen()
mongodbPoll = mongodb.MongoPoll();

travelTime = vegvesen.getTravelTime()

lastItem = mongodbPoll.getLastTravelTime()
diff = travelTime.diff(lastItem)
logging.info(diff)

messaging = messaging.VegvesenMessages()
messaging.publishChanges(diff)

mongodbPoll.addTravelTime(travelTime)

