#!/bin/python
from flask import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getHierarchy', methods=['GET'])
def getHierarchy():
	return jsonify(
		getHierarchy="SOOOOOOO MANY FILES"
    )


@app.route('/getChanges', methods=['GET'])
def getChanges():

    if 'lastChange' in request.args:
    	lastChange = request.args['lastChange']
    else:
    	lastChange = False

    if (lastChange):
    	return jsonify(
			lastChange=lastChange
        )

    return jsonify(
			error="lastChange not set"
        ), 422

@app.route('/getFile', methods=['GET'])
def getFile():

	if 'fileId' in request.args:
		fileId = request.args['fileId']
	else:
		fileId = False

	if 'lastChange' in request.args:
		lastChange = request.args['lastChange']
	else:
		lastChange = False

	if (fileId and lastChange):
		return jsonify(
			lastChange=lastChange,
			fileId=fileId
		)

	return jsonify(
			error="lastChange/fileId not set"
	    ), 422


@app.route('/pushFile', methods=['GET', 'POST'])
def pushFile():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')

if __name__ == '__main__':
	app.debug = True
	app.run()