from flask import Flask, render_template, request
from pymongo import Connection
import pulls
import builds
import githubAPI
import configuration

app = Flask(__name__)

connection = Connection()
monDB = connection['bitcointesting']
github = githubAPI.GithubAPI(configuration.github_user, configuration.github_password)

@app.route("/", methods=['GET', 'POST'])
def home():
    pulls = monDB['pulls'].find({'status':'active'})
    #we have to add the nightly builds of the master branch, and have that as the first selectable option
    return render_template('home.html', pulls)

@app.route("download", methods=['POST'])
def download():
    binary = request.form['binary']
    return render_template('download.html', binary)

def updateDB():
    #Grab the PB
    try:
        p = pulls.grabPulls()
        b = builds.grabBuilds()
        print "Pulls updated: " + p + " Builds updated: " + b
    except Exception as e:
        print "Could not update the DB with new pulls / builds: ", e
    
    #Add the Jelly
    try:
        pulls = monDB['pulls'].find({'status':'active'})
        for pull in pulls:
            build = monDB['builds'].find_one({'pullnum':pull['pullnum'], 'status':'active'})
            monDB['pulls'].update({'pullnum':pull['pullnum']}, {'$set':{'binary':build['url']}})
    except Exception as e:
        print "We ran out of bread: ", e
        
    
if __name__ == "__main__":
    app.run()
    
    #auth to github
    #get all the open pull requests from github bitcoin/bitcoin that can be automatically merged.
    #store them in the db. Name, author, date
    #grab the build's file urls from matt's jenkins
    #store them in the db. _id, url, system (win32, win64, ubuntu, etc.)