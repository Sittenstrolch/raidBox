from copy import copy

class FileTreeMap(object):
    """docstring for FileTreeMap"""
    
    def __init__(self, files={}, path_index={}):
        super(FileTreeMap, self).__init__()
        self.new_id = -len(files) - 1

        # id to file path
        self.files = files

        # maps path to file ID
        # todo get paths
        self.path_index = path_index

        self.deleted_files = set()
        self.modified_files = set()

    def add(self, id, path):
        self.files[id] = path
        self.path_index[path] = id

    def getPath(self, id):
        return self.files[id] if id in self.files else None

    def getByPath(self, path):
        return self.files[self.path_index[path]] if path in self.path_index else None

    def move(self, path, newPath):
        id = self.getId(path)
        del self.path_index[path]

        self.files[id] = newPath
        self.path_index[newPath] = id

    def create(self, path):
        # check if there exists a file at that path
        id = self.getId(path)
        if id:
            # if the file was deleted in this pass
            # re-create it and set it as modified
            if id in self.deleted_files:
                self.deleted_files.remove(id)
                self.modified_files.add(id)
        else:
            self.files[self.new_id] = path
            self.path_index[path] = self.new_id
            self.new_id -= 1

    def delete(self, path):
        self.deleted_files.add(self.getId(path))

    def modify(self, path):
        self.modified_files.add(self.getId(path))

    def getId(self, path):
        return self.path_index[path] if path in self.path_index else None

    def clone(self):
        return FileTreeMap(copy(self.files), copy(self.path_index))

    def contains(self, path):
        return self.getId(path) is not None

    def applyFileSystemEvent(self, evt):
        if evt.event_type == "created":
            self.create(evt.src_path)
        elif evt.event_type == "deleted":
            self.delete(evt.src_path)
        elif evt.event_type == "moved":
            self.move(evt.src_path, evt.dest_path)
        elif evt.event_type == "modified":
            self.modify(evt.src_path)
        else:
            print "SHOULD NOT HAPPEN", evt.event_type





