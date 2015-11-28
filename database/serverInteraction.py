import sqlite3

#looks for the connection to the db within the directory of execution
class serverDbConnector:
    def __init__(self):
        self.connection = sqlite3.connect('server.db')

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

    def addLog(self, fileId, action):
        self.connection.execute('''
            Insert into Log (fileId, action)
            VALUES (? ,?)
        ''', (fileId, action))
        self.connection.commit()

    def addLogWithTimestamp(self, timestamp, fileId, action):
        self.connection.execute('''
            Insert into Log (timestamp, fileId, action)
            VALUES (? ,?, ?)
        ''', (timestamp, fileId, action))
        self.connection.commit()

    def deleteLog(self, logId):
        self.connection.execute('''DELETE FROM Log WHERE id=?''',(str(logId)))
        self.connection.commit()

conn = serverDbConnector()
conn.addLog(1234533, 'move')
print conn.getLogs()
conn.deleteLog('3')
print conn.getLogs()
