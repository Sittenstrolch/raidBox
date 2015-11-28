import os
import copy
import time
import logging
from watchdog.observers import Observer
from watchdog.events import *


class SCSFileChangeLog(object):
    """docstring for SCSFileChangeLog"""
    def __init__(self):
        super(SCSFileChangeLog, self).__init__()
        self.changes = set()

    def addChange(self, timestamp, event):
        self.changes.add((timestamp, event))

    def getChanges(self):
        return self.changes

    def getChangesPerFile(self):
        file_changes = {}
        for ts, event in self.changes:
            if not event.src_path in file_changes:
                file_changes[event.src_path] = [(ts, event)]
            else:
                file_changes[event.src_path].append((ts, event))

        return file_changes

    def printChanges(self):
        changes = self.getChangesPerFile()
        if len(changes) > 0:
            print "%d files changed" % len(changes)
            for path in changes:
                print "\t", path
                for ts, event in changes[path]:
                    print "\t\t", time.strftime("%H:%M:%S", time.gmtime(ts)), event
        else:
            print "No Changes"
        

class SCSFileObserver(FileSystemEventHandler):
    """
        SCSFileObserver
        path - The path for which we are tracking all changes
        files - An existing map of file, which maps the full path to it's ID (None if it has no ID yet)
    """
    def __init__(self, path, files):
        super(SCSFileObserver, self).__init__()
        self.path = path
        self.changelog = SCSFileChangeLog()
        self.files = files

    def run(self):
        self.getInitialFileList()

        # initialize the live observer (watchdog)
        # runs the observer in a separate thread
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.observer.start() 
        print "observing ", self.path

    def getInitialFileList(self):
        for root, dirs, files in os.walk(self.path):
            # check if all existing files have IDs
            for filename in files:
                fullpath = os.path.join(root, filename)
                if not self.files.contains(fullpath):
                    self.files.create(fullpath)

            # check if all existing dirs have IDs
            for filename in dirs:
                fullpath = os.path.join(root, filename)
                if not self.files.contains(fullpath):
                    self.files.create(fullpath)

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()

    # called whenever file event is detected
    def on_any_event(self, event):
        print event.event_type, event.is_directory, event.src_path
        timestamp = time.time()

        if event.event_type == "modified" and event.is_directory:
            # we don't care when a directory is modified
            # this just means, that something changed within that directory
            return

        self.changelog.addChange(timestamp, event)

    def getChanges(self):
        return self.changelog.getChanges()

