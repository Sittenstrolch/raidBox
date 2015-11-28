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
        self.file_list = FileList()

    def run(self):
        print "running SCSClient"
        self.connector = ServerConnector(hostname="localhost", port=5000)
        self.db = ClientDbConnector("../client.db")

        if not os.path.exists(self.path):
            self.initializeCloudStorage()

        self.observeChanges()

    def observeChanges(self):
        self.observer = SCSFileObserver(self.path, self.file_list)
        self.observer.run()

    def stop(self):
        self.observer.stop()
        self.observer.join()

        print "\nstopped SCSClient"

    def downloadFile(self, id):
        r = self.connector.getFile(id, 0, True)
        data = r["response"]["data"]

        path = data["filename"]
        fullpath = os.path.join(self.path, path)

        with open(fullpath, "wb") as fh:
            fh.write(data["content"])

        self.file_list.files[id] = fullpath
        self.file_list.path_index[fullpath] = id


    def initializeCloudStorage(self):
        print "initializing cloud storage in '%s'" % (self.path)
        os.makedirs(self.path)

        # get all files that currently exist on the remote host
        response = self.connector.getHierarchy()
        data = response["response"]["data"]

        #store files to local db
        self.db.addFiles(data);

        for info in data:
            self.downloadFile(info["id"])

    def sync(self):
        print "synchronizing"
        # replay the changes on our file tree
        # to identify the exact changes
        local_changes = copy.copy(self.observer.getChanges())
        local_changes = sorted(local_changes)
        new_list = self.file_list.clone()

        for timestamp, event in local_changes:
            new_list.applyFileSystemEvent(event)

        print self.file_list.files, self.file_list.deleted_files
        print new_list.files, new_list.deleted_files

        # synching
        for fileId in new_list.files:
            if fileId < 0 and not fileId in new_list.deleted_files:
                print "New File Created: %s" % (new_list.getPath(fileId))

            if new_list.getPath(fileId) != self.file_list.getPath(fileId):
                print "File Moved: %s (from %s)" % (new_list.getPath(fileId), self.file_list.getPath(fileId))

        for fileId in new_list.deleted_files:
            if fileId > 0: # only delete files that already have been synched
                print "File deleted: %s" % (new_list.getPath(fileId))

        for fileId in new_list.modified_files:
            print "File modified: %s" % (new_list.getPath(fileId))

        self.file_list = new_list





