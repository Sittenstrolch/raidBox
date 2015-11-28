
import requests

class ServerConnector(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.url = 'http://' + hostname + ':' + str(port) + '/'

    def getHierarchy(self):
        r = requests.get(self.url + 'getHierarchy')
        return r.json()

    def getChanges(self, lastChange = None):
        payload = {'lastChange': lastChange}
        r = requests.get(self.url + 'getChanges', params=payload)
        return {
            'success': r.status_code == requests.codes.ok,
            'response': r.json()
        }