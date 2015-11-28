#!/bin/python
from flask import *
import io
import os
from ServerDbConnector import ServerDbConnector

# cd to the server/ directory
SERVER_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(SERVER_PATH)



app = Flask(__name__)
db = ServerDbConnector("../server.db")

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

    fileName = request.headers["filename"]

    parent = None
    if 'parent' in request.headers:
        parent = request.headers["parent"]

    fileId = None
    fileType = request.headers["type"]
    withContent = request.headers["withContent"]
    lastChange = request.headers["lastChange"]
    fileHash = request.headers["hash"]

    if 'id' in request.headers:
        fileId = request.headers['id']

    latestLog = db.getLatestLog()

    if request.method == 'POST':
        if latestLog == {} or latestLog == request.headers["lastChange"]:
            # New File created
            if fileId == None:
                newId = db.addFile(fileName, parent, fileType, fileHash)
                file = request.files[fileName]
                filePath = "files/" + str(newId)
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                file.save(filePath+"/head")
                return jsonify(
                        {
                            "data": {
                                'id': newId
                            }
                        }
                    ), 200
            else:
                db.updateFile({'name': fileName, 'parent': parent, 'type': fileType, 'hash': fileHash})
                file = request.files[fileName]
                filePath = "files/" + str(newId)
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                file.save(filePath+"/head")
                return jsonify(
                        {
                            "data": {
                                'id': fileId
                            }
                        }
                    ), 200
        else:
            return jsonify(
                    {
                        'error': 'get the new changes first'
                    }
                ), 422

if __name__ == '__main__':
    app.debug = True
    app.run()
