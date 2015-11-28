#!/bin/python
from flask import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getHierarchy', methods=['GET'])
def getHierarchy():
    return jsonify(
        {
            data: {
                getHierarchy: "SOOOOOOO MANY FILES"
            }
        }
    )


@app.route('/getChanges', methods=['GET'])
def getChanges():

    if 'lastChange' in request.args:
        lastChange = request.args['lastChange']
    else:
        lastChange = False

    if (lastChange):
        return jsonify(
            {
                'data': {
                    'changes': "SOOOOOOO MANY CHANGES"
                }
            }
        )

    return jsonify(
            {
                'error': 'lastChange not set'
            }
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
            {
                'data': {
                    'file': "LOOK AT DAT FILE"
                }
            }
        )

    return jsonify(
            {
                'error': 'lastChange/fileId not set'
            }
        ), 422


@app.route('/pushFile', methods=['GET', 'POST'])
def pushFile():
    print request.headers
    if request.method == 'POST':
        filesUploaded = request.files.keys()
        for fileName in filesUploaded:
            file = request.files[fileName]
            file.save(fileName)

if __name__ == '__main__':
    app.debug = True
    app.run()
