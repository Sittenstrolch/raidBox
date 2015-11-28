import os
import copy
from SCSFileObserver import SCSFileObserver
from ServerConnector import ServerConnector
from ClientDbConnector import ClientDbConnector
from FileList import FileList

class SCSClient(object):
    """docstring for SCSClient"""
    def __init__(self, path):
        super(SCSClient, self).__init__()
        self.path = path
        self.files = FileList()

    def run(self):
        print "running SCSClient"
        self.connector = ServerConnector(hostname="localhost", port=5000)
        self.db = ClientDbConnector("../client.db")

        if not os.path.exists(self.path):
            self.initializeCloudStorage()

        self.observeChanges()

        print self.connector.getFile(lastChange=1, fileId=1);

    def observeChanges(self):
        self.observer = SCSFileObserver(self.path, self.files)
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
        print "synchronizing"
        # replay the changes on our file tree
        # to identify the exact changes
        local_changes = copy.copy(self.observer.getChanges())
        local_changes = sorted(local_changes)
        new_files = self.files.clone()

        for timestamp, event in local_changes:
            new_files.applyFileSystemEvent(event)
        
        print self.files.files, self.files.deleted_files
        print new_files.files, new_files.deleted_files

        
