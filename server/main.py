#!/bin/python
from flask import *
import io
from ServerDbConnector import ServerDbConnector

app = Flask(__name__)
db = ServerDbConnector()

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

        response = make_response(send_file("files/1/head", as_attachment=True, attachment_filename="daria.png"))
        response.headers['X-fileId'] = '1'
        response.headers['X-fileName'] = "daria.png"
        response.headers['X-fileParent'] = "null"
        response.headers['X-fileType'] = "file"
        response.headers['X-fileHash'] = "BDFASRHF7894yhfnsofih89"
        return response

    return jsonify(
            {
                'error': 'lastChange/fileId not set'
            }
        ), 422


@app.route('/pushFile', methods=['GET', 'POST'])
def pushFile():
    print request.headers
    db.getLogs()

    if request.method == 'POST':
        filesUploaded = request.files.keys()
        for fileName in filesUploaded:
            file = request.files[fileName]
            file.save(fileName)

if __name__ == '__main__':
    app.debug = True
    app.run()
