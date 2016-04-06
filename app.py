from flask import Flask
import flask
import os
import pymongo
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
	ret['one'] = collection.find().limit(1).sort('{$natural:-1}')[0]['publicationTime']
	return flask.jsonify(ret)

if __name__ == '__main__':
    app.debug = True
    app.run()

