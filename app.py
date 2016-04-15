from flask import Flask
import flask
import mongodb
app = Flask(__name__)


@app.route('/')
def hello():
	mongoPoll = mongodb.MongoPoll()
	ret = mongoPoll.getStats()
	return flask.jsonify(ret)

if __name__ == '__main__':
	app.debug = True
	app.run()

