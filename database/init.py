#!/usr/bin/python

import sqlite3

connServer = sqlite3.connect('server.db')
connClient = sqlite3.connect('client.db')

def createServerFileTable ():
    connServer.execute('''create table File(
        id INTEGER PRIMARY KEY,
        name TEXT,
        parent TEXT,
        type CHAR(10),
        hash TEXT,
        deleted BOOLEAN default 0
    )''')

def createClientFileTable ():
    connClient.execute('''create table File(
        id INTEGER PRIMARY KEY,
        name TEXT,
        parent TEXT,
        type CHAR(10),
        hash TEXT
    )''')


def createLogTable (conn):
    conn.execute('''create table Log(
        id INTEGER PRIMARY KEY,
        timestamp INT default (strftime(\'%s\',\'now\')),
        fileId TEXT,
        action CHAR(40)
    )''')

createServerFileTable()
createClientFileTable()
createLogTable(connServer)
createLogTable(connClient)
