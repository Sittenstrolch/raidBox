import os
import sqlite3

#looks for the connection to the db within the directory of execution
class ServerDbConnector:
    def __init__(self, path):
        if not os.path.exists(path):
            raise Exception("can not find sqlite database")

        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.connection.cursor()

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
        return true

    def addFile(self, name, parent, fileType, fileHash):
        self.cursor.execute('''
            Insert into File (name, parent, type, hash)
            VALUES (? ,?, ?, ?)
        ''', (name, str(parent), fileType, fileHash))
        self.connection.commit()
        return self.cursor.lastrowid

    def deleteFile(self, fileId):
        self.updateFile(fileId, deleted, 1)
        return

    def updateFile(self, file):
        self.cursor.execute(
            "Update File set name=?, parent=?, type=?, hash=? where id=?",
            (file['filename'], file['parent'], file['type'], file['hash'], str(file["id"]))
        )
        self.connection.commit()
        return True

    def getFile(self, fileId):
        cursor = self.connection.execute(
            "Select id, name, parent, type, hash, deleted from File Where id=?",
            (str(fileId))
        )
        file = {}
        for row in cursor:
            file = {
                "id": row[0],
                "name": row[1],
                "parent": row[2],
                "type": row[3],
                "hash": row[4],
                "deleted": True if row[5]==1 else False
            }
        return file

    def getFiles(self):
        cursor = self.connection.execute("Select id, name, parent, type, hash, deleted from File")
        files = []
        for row in cursor:
            file = {
                "id": row[0],
                "name": row[1],
                "parent": row[2],
                "type": row[3],
                "hash": row[4],
                "deleted": True if row[5]==1 else False
            }
            files.append(file)
        return files
