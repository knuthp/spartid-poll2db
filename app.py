from flask import Flask
from flask import request
import flask
import mongodb
from bson import json_util

app = Flask(__name__)


@app.route('/')
def hello():
	mongoPoll = mongodb.MongoPoll()
	ret = mongoPoll.getStats()
	return flask.jsonify(ret)

@app.route('/history')
def history():
	mongoPoll = mongodb.MongoPoll()
	query = {}
	limit = request.args.get('limit')
	if limit : 
		query['limit'] = int(limit)
	history = mongoPoll.getHistory(query)
	return json_util.dumps(history)

if __name__ == '__main__':
	app.debug = True
	app.run()

