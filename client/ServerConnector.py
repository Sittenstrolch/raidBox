
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

        local_filename = "example_data/daria.png"

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        # return {
        #     'success': r.status_code == requests.codes.ok,
        #     'response': r.json()
        # }

    def pushFile(self, fileId = None, lastChange = None):
        # payload = {'lastChange': lastChange, 'fileId': fileId}
        # r = requests.get(self.url + 'getChanges', params=payload)
        # return {
        #     'success': r.status_code == requests.codes.ok,
        #     'response': r.json()
        # }

        return {'success': true}