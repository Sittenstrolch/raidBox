import os
from SCSFileObserver import SCSFileObserver
from ServerConnector import ServerConnector

class SCSClient(object):
    """docstring for SCSClient"""
    def __init__(self, path):
        super(SCSClient, self).__init__()
        self.path = path

    def run(self):
        print "running SCSClient"
        self.connector = ServerConnector(hostname="localhost", port=5000)

        if not os.path.exists(self.path):
            self.initializeCloudStorage()

        self.observeChanges()

    def observeChanges(self):
        self.observer = SCSFileObserver(self.path)
        self.observer.run()

    def stop(self):
        self.observer.stop()
        self.observer.join()

        print "\nstopped SCSClient"

    def initializeCloudStorage(self):
        print "initializing cloud storage in '%s'" % (self.path)
        os.makedirs(self.path)
        