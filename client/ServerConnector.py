
import requests

class ServerConnector(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.url = 'http://' + hostname + ':' + str(port) + '/'

    def getHierarchy(self):
        r = requests.get(self.url + 'getHierarchy')
        return {
            'success': r.status_code == requests.codes.ok,
            'response': r.json()
        }

    def getChanges(self, lastChange = None):
        payload = {'lastChange': lastChange}
        r = requests.get(self.url + 'getChanges', params=payload)
        return {
            'success': r.status_code == requests.codes.ok,
            'response': r.json()
        }

    def getFile(self, fileId = None, lastChange = None, withContent = False):
        payload = {'lastChange': lastChange, 'fileId': fileId, 'withContent': withContent}
        r = requests.get(self.url + 'getFile', params=payload, stream=True)

        if (r.status_code == requests.codes.ok):

            return {
                'success' : True,
                'response' : {
                    'data': {
                        'id' : r.headers['X-fileId'],
                        'filename': r.headers['X-fileName'],
                        'parent': r.headers['X-fileParent'],
                        'type': r.headers['X-fileType'],
                        'hash': r.headers['X-fileHash'],
                        'content': r.content
                    }
                }
            }

        return {
            'success': r.status_code == requests.codes.ok,
            'response': r.json()
        }

    def pushFile(self, file, lastChange = None, withContent = True):
        payload = file

        data = file["content"]
        del file["content"]
        headers = file
        headers['lastChange'] = lastChange
        headers['withContent'] = withContent

        r = requests.post(self.url + 'pushFile', files=[(file['filename'], data)], headers=headers)
        return {
            'success': r.status_code == requests.codes.ok,
            'response': r.json()
        }

