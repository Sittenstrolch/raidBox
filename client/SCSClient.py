import os
from SCSFileObserver import SCSFileObserver
from ServerConnector import ServerConnector
from ClientDbConnector import ClientDbConnector

class SCSClient(object):
    """docstring for SCSClient"""
    def __init__(self, path):
        super(SCSClient, self).__init__()
        self.path = path

    def run(self):
        print "running SCSClient"
        self.connector = ServerConnector(hostname="localhost", port=5000)
        self.db = ClientDbConnector("../client.db")

        if not os.path.exists(self.path):
            self.initializeCloudStorage()

        self.observeChanges()

        print self.connector.getHierarchy();

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

        # get all files that currently exist on the remote host
        response = self.connector.getHierarchy()
        print response
        # TODO: initialize the directory with all files from remote

    def sync(self):
        # 1. getChanges
        # excerpt of the log table
        response = self.connector.getChanges()
        # changes = response["data"]
        changes = []

        # todo: process the changes
        # find out what files have to be downloaded

        # 2. getFile
        for change in changes:
            pass


        # 3. push changes