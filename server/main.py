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
            'data': db.getFiles()
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

        file = db.getFile(fileId)

        response = make_response(send_file("files/" + str(fileId) + "/head", as_attachment=True, attachment_filename=file["name"]))
        response.headers['X-fileId'] = str(fileId)
        response.headers['X-fileName'] = file["name"]
        response.headers['X-fileParent'] = file["parent"]
        response.headers['X-fileType'] = file["type"]
        response.headers['X-fileHash'] = file["hash"]
        return response

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
