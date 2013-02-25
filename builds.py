from pymongo import Connection

connection = Connection()
monDB = connection['bitcointesting']

def grabBuilds():
    newBuilds = ["Get the builds somehow"]
    i = 0
    for build in newBuilds:
        monDB['builds'].update({'bid':build['id']}, {'$set':{'name':build['title'], 'pullnum':build['pullnum'], 'win32url':build['url']}}, True)
        i++
    return str(i)