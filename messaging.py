import paho.mqtt.client as mqtt
import os
import urlparse
import logging



class VegvesenMessages:
    def __init__(self):
        self.mqttc = mqtt.Client("vegvesen_pub")
        # Uncomment to enable debug messages
        #mqttc.on_log = on_log
        
        # Parse CLOUDMQTT_URL (or fallback to localhost)
        url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://iot.eclipse.org:1883')
        url = urlparse.urlparse(url_str)
        
        # Connect
        if url.username is not None:
            self.mqttc.username_pw_set(url.username, url.password)

            self.mqttc.connect(url.hostname, url.port)



    def publishChanges(self, changes):
        for d in changes:
            legId = d['new']['id']
            topicPrefix = "spartid/vegvesen/realtime/" + legId    
            # Publish a message
            if d['new']['travelTime'] != d['old']['travelTime']: 
                travelTime = d['new']['travelTime']
                topic =  topicPrefix + "/travelTime"
                self.mqttc.publish(topic, str(travelTime))

            if d['new']['travelTimeType'] != d['old']['travelTimeType']: 
                travelTimeType = d['new']['travelTimeType']
                topic =  topicPrefix + "/travelTimeType"
                self.mqttc.publish(topic, str(travelTimeType))
 
            if d['new']['travelTimeTrendType'] != d['old']['travelTimeTrendType']: 
                travelTimeTrendType = d['new']['travelTimeTrendType']
                topic =  topicPrefix + "/travelTimeTrendType"
                self.mqttc.publish(topic, str(travelTimeTrendType))
        
        # establish a ten-second timeout
        self.mqttc.loop(10)
        logging.info("Processed diffs.len=%s", len(changes))
        
        

