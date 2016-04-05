import os
import requests

url = 'https://www.vegvesen.no/ws/no/vegvesen/veg/trafikkpublikasjon/reisetid/1/GetTravelTimeData'
username = os.environ.get('VEGVESEN_USERNAME')
password = os.environ.get('VEGVESEN_PASSWORD')
r = requests.get(url, auth=(username, password))

print (r.text)
