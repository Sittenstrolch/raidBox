#!/usr/bin/python

import sqlite3

connServer = sqlite3.connect('server.db')
connClient = sqlite3.connect('client.db')

print "Opened database successfully";

def createServerFileTable ():
    connServer.execute('''create table File(
        id int Primary Key,
        name text,
        parent text,
        type char(10),
        hash text
    )''')

def createClientFileTable ():
    connClient.execute('''create table File(
        id INT Primary Key,
        name text,
        parent text,
        type char(10),
        hash text
    )''')


def createLogTable (conn):
    conn.execute('''create table Log(
        id int Primary Key,
        timestamp int,
        fileId text,
        action char(40)
    )''')

createServerFileTable()
createClientFileTable()
createLogTable(connServer)
createLogTable(connClient)
