#this is a file library
from pathlib import Path
import os
import json
import bcrypt

DATADIR="data"
SALT="7a743ffa0b39e7faf7e6be71eacc9af906da3cff6f8c3c54ae5e26d8a460f50c"

def listFiles():
    files = []
    for t in os.listdir(DATADIR):
        if t.endswith(".json"):
            files.append(t)
    return files

#this lists all pages
def getPages(userFile):
    try:
        with file(userFile, "r") as file:
            userData = json.load(file)
            pages = []
            for page in userData.pages
                pages.append(page.meta)
        return pages
    except:
        return -1

#loads the data for a page
def loadData(userFile,pageName):
    try:
        with file(userFile, "r") as file:
            userData = json.load(file)
            try:
                return userData.pages[pageName]
            except:
                return -2
    except:
        return -1

#write changes to a page
def writeData(userFile, pageName, data):
    try:
        with file(userFile, "r") as file:
            userData = json.load(file)
            try:
                userData.pages[pageName] = data
                return 0
            except:
                return -2
    except:
        return -1

#set Password
def setPassword(userFile, passwd):
    try:
        with file(userFile, "r") as file:
            userData = json.load(file)
            try:
                userData.passwd = bcrypt.hashpw(passwd, SALT)
                return 0
            except:
                return -2
    except:
        return -1

def createUser(userFile, passwd):
    if userFile.endswith(".json"):
        try:
            with open(userFile, 'w') as file:
                userData = {}
                userData.pages = {}
                userData.passwd = bcrypt.hashpw(passwd, SALT)
                userData.lastLogonTime = "never"
                userData.displayName = "user"
                return 0
        except:
            return -1
    else:
        return -2

