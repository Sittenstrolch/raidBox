import os
import copy
from SCSFileObserver import SCSFileObserver
from ServerConnector import ServerConnector
from ClientDbConnector import ClientDbConnector
from FileTreeMap import FileTreeMap

class SCSClient(object):
    """docstring for SCSClient"""
    def __init__(self, path):
        super(SCSClient, self).__init__()
        self.path = path

        self.tree = FileTreeMap()

    def run(self):
        print "running SCSClient"
        self.connector = ServerConnector(hostname="localhost", port=5000)
        self.db = ClientDbConnector("../client.db")

        if not os.path.exists(self.path):
            self.initializeCloudStorage()
        else:
            # load the file info from the database
            infos = self.db.getFiles()
            infoMap = { info["id"]: info for info in infos }

            # print infoMap
            for info in infos:
                parts = [info["name"]]

                while info["parent"]:
                    info = infoMap[info["parent"]]
                    parts.append(info["name"])

                path = "/".join(parts)
                fullpath = os.path.join(self.path, path)
                self.tree.index(info["id"], fullpath)

        self.observeChanges()

    def observeChanges(self):
        self.observer = SCSFileObserver(self.path, self.tree)
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

        # store the information in our file list
        self.tree.index(id, fullpath)


    def initializeCloudStorage(self):
        print "initializing cloud storage in '%s'" % (self.path)
        os.makedirs(self.path)

        # get all files that currently exist on the remote host
        response = self.connector.getHierarchy()
        data = response["response"]["data"]

        #store files to local db
        self.db.truncateFiles()
        self.db.addFiles(data)

        for info in data:
            self.downloadFile(info["id"])


    def sync(self):
        print "synchronizing"
        # replay the changes on our file tree
        # to identify the exact changes
        local_changes = copy.copy(self.observer.getChanges())
        local_changes = sorted(local_changes)
        new_list = self.tree.clone()

        for timestamp, event in local_changes:
            new_list.applyFileSystemEvent(event)

        print self.tree.files, self.tree.deleted_files
        print new_list.files, new_list.deleted_files

        # synching
        for fileId in new_list.files:
            if fileId < 0 and not fileId in new_list.deleted_files:
                # CREATE NEW FILE
                print "New File Created: %d : %s" % (fileId, new_list.getPath(fileId))

                path = new_list.getPath(fileId)
                with open(path, "rb") as fh:
                    data = {
                        "filename": os.path.basename(path),
                        "parent": 0,
                        "type": "file",
                        "hash": "XXX",
                        "content": fh.read()
                    }
                    response = self.connector.pushFile(data, 0, True)
                    id = response["response"]["data"]["id"]

                    self.db.addFile(id, data["filename"], data["parent"], data["type"], data["hash"])

                    del new_list.files[fileId]
                    new_list.files[id] = path
                    new_list.path_index[path] = id



            if new_list.getPath(fileId) != self.tree.getPath(fileId):
                print "File Moved: %d : %s (from %s)" % (fileId, new_list.getPath(fileId), self.tree.getPath(fileId))

        for fileId in new_list.deleted_files:
            if fileId > 0: # only delete files that already have been synched
                print "File deleted: %d : %s" % (fileId, new_list.getPath(fileId))

        for fileId in new_list.modified_files:
            print "File modified: %d : %s" % (fileId, new_list.getPath(fileId))

        self.tree = new_list





