from flask import Flask, render_template, request
from pymongo import Connection
import pulls, builds, githubAPI, configuration

app = Flask(__name__)

connection = Connection()
monDB = connection['bitcointesting']

owner = configuration.github_owner
repo = configuration.github_repo
bot_user = configuration.bot_user

@app.route("/", methods=['GET', 'POST'])
def home():
    pulls = monDB['pulls'].find({'status':'active'})
    #we have to add the nightly builds of the master branch, and have that as the first selectable option
    return render_template('home.html', pulls)

@app.route("download", methods=['POST'])
def download():
    binary = request.form['binary']
    return render_template('download.html', binary)


#Grab all the comments on open pull requests, and filter out those made by the bot
def get_bot_comments():
    pull_nums=githubAPI.get_pull_nums(owner,repo)
    bot_comments = []
    
    for pull in pull_nums:
        bot_comments.append(githubAPI.get_user_comments(owner,repo,pull,bot_user))
    
    return bot_comments
    

#Grab all the binaries from the bots comments and enforce 1:pull 
def get_binaries():
    comments = get_bot_comments()
    binaries = []
    return binaries    
    

#save all the shit in the db
def updateDB():
    #Grab the PB
    try:
        p = githubAPI.get_pulls('bitcoin','bitcoin')
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
    
    #get all the open pull requests from github bitcoin/bitcoin that can be automatically merged.
    #store them in the db. Name, author, date
    #grab the build's file urls from matt's jenkins
    #store them in the db. _id, url, system (win32, win64, ubuntu, etc.)