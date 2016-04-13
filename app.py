from flask import Flask
import flask
import os
import pymongo
from datetime import datetime
from datetime import timedelta
from dateutil import tz
app = Flask(__name__)


@app.route('/')
def hello():
	mongoUri = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/testdb')
	print('Using mongodb url=%s', mongoUri)
	client = pymongo.MongoClient(mongoUri)
	db = client.get_default_database()
	collection = db.vegvesen_traveltime
	ret = {}
	ret['count'] = str(collection.count())
	ret['one'] = collection.find().sort("$natural", -1).limit(1)[0]['publicationTime']
	today = datetime.utcnow().date()
	yesterday = today - timedelta(1)
	start = datetime(today.year, today.month, today.day, tzinfo=tz.tzutc())
	yesterdayStart = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=tz.tzutc())
	ret['today'] = { 'count' : collection.find({"publicationTime" : { "$gte" : start} }).count() }
	ret['yesterday'] = { 'count' : collection.find({"publicationTime" : { "$gte" : yesterdayStart, "$lte" : start,} }).count() }
	return flask.jsonify(ret)

if __name__ == '__main__':
	app.debug = True
	app.run()

