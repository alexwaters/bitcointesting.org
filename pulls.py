from pymongo import Connection

connection = Connection()
monDB = connection['bitcointesting']

def grabPulls(): #grab the pulls somehow
    newPulls = [{'pullnum':'2338', 'title':'Short-circuit bloom checking if we will always return true.', 'author':'TheBlueMatt'}, {2:'parse them awesomely'}]
    i = 0
    for pull in newPulls:
        monDB['pulls'].update({'pullnum':pull['pullnum']}, {'$set':{'name':pull['title'], 'url':pull['url'], 'author':pull['author']}}, True)
        i++
    return str(i)