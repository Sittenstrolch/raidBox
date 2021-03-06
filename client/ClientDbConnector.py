import sqlite3
import os

#looks for the connection to the db within the directory of execution
class ClientDbConnector:
    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("can not find sqlite database")

        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.path = path

        print "connected to database"

    def getLogs(self):
        cursor = self.connection.execute('Select id, timestamp, fileId, action From Log')
        logs = []
        for row in cursor:
            log = {
                "id": row[0],
                "timestamp": row[1],
                "fileId": row[2],
                "action": row[3]
            }
            logs.append(log)
        return logs

    def getLog(self, logId):
        cursor = self.connection.execute('Select id, timestamp, fileId, action From Log Where id=?',(str(logId)))
        log = {}
        for row in cursor:
            log = {
                "id": row[0],
                "timestamp": row[1],
                "fileId": row[2],
                "action": row[3]
            }
        return log

    def getLatestLog(self):
        cursor = self.connection.execute('''
            Select id, timestamp, fileId, action
            From Log
            Where timestamp=(
                Select MAX(timestamp)
                From Log
            )

        ''')
        log = {}
        for row in cursor:
            log = {
                "id": row[0],
                "timestamp": row[1],
                "fileId": row[2],
                "action": row[3]
            }
        return log

    def getLogsSince(self, timestamp):
        cursor = self.connection.execute(
            'Select id, timestamp, fileId, action From Log Where timestamp > ?',
            (str(timestamp))
        )
        logs = []
        for row in cursor:
            log = {
                "id": row[0],
                "timestamp": row[1],
                "fileId": row[2],
                "action": row[3]
            }
            logs.append(log)
        return logs

    def addLog(self, fileId, action):
        self.cursor.execute('''
            Insert into Log (fileId, action)
            VALUES (? ,?)
        ''', (fileId, action))
        self.connection.commit()
        return self.cursor.lastrowid

    def deleteLog(self, fileId):
        self.cursor.execute('''
            Delete from Log where id=?
        ''', (str(logId)) )
        self.connection.commit()
        return self.cursor.lastrowid

    def addLogWithTimestamp(self, timestamp, fileId, action):
        self.connection.execute('''
            Insert into Log (timestamp, fileId, action)
            VALUES (? ,?, ?)
        ''', (timestamp, fileId, action))
        self.connection.commit()
        return self.cursor.lastrowid

    def deleteLog(self, logId):
        self.cursor.execute('''DELETE FROM Log WHERE id=?''',(str(logId)))
        self.connection.commit()
        return Tsrue

    def addFile(self, fileId, name, parent, type, hash):
        self.cursor.execute('''
            Insert into File (id, name, parent, type, hash)
            VALUES (?, ? ,?, ?, ?)
        ''', (fileId, name, parent, type, hash))
        self.connection.commit()
        return self.cursor.lastrowid

    def addFiles(self, files):
        for file in files:
            self.addFile(file['id'], file['name'], file['parent'], file['type'], file['hash'])

    def truncateFiles(self):
        self.cursor.execute("DELETE FROM File")
        self.connection.commit()
        return True

    def deleteFile(self, fileId):
        self.updateFile(fileId, deleted, 1)
        return True

    def updateFile(self, fileId, property, value):
        self.cursor.execute(
            "Update File set ?=? where id=?",
            (property, value, str(fileId))
        )
        self.connection.commit()
        return True

    def getFile(self, fileId):
        cursor = self.connection.execute(
            "Select id, name, parent, type, hash from File Where id=?",
            (str(fileId))
        )
        file = {}
        for row in cursor:
            file = {
                "id": row[0],
                "name": row[1],
                "parent": row[2],
                "type": row[3],
                "hash": row[4]
            }
        return file

    def getFiles(self):
        cursor = self.connection.execute("Select id, name, parent, type, hash from File")
        files = []
        for row in cursor:
            file = {
                "id": row[0],
                "name": row[1],
                "parent": row[2],
                "type": row[3],
                "hash": row[4]
            }
            files.append(file)
        return files
