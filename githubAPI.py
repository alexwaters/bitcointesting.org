import requests,json,pprint
import configuration

v = configuration.verbose
    
pp = pprint.PrettyPrinter(indent=4)

#get the first 100 of the open pull requests for a repo, and return the issue urls
def get_pulls(owner,repo):
    #/repos/:owner/:repo/pulls
    count = 0
    pulls = []
    
    request = requests.get('https://api.github.com/repos/%s/%s/pulls?per_page=100' % owner, repo)
    content = json.loads(request.content)
    
    for pull in content:
        pulls.append(pull)
        count+=1
    
    if v: print ('\n%s open pull requests.' % str(count))
    return pulls


def get_pull_comments(owner,repo,pull):
    count = 0
    request = requests.get('https://api.github.com/repos/%s/%s/issues/%s/comments' % owner, repo, pull)
    comments = json.loads(request.content)
    
    for comment in comments: count+=1
    if v: print ('\n%s comments in pull number %s.' % str(count),pull)
    return comments


#get the first 100 of the open pull requests for a repo, and return the issue urls
def get_pull_nums(owner,repo):
    #/repos/:owner/:repo/pulls
    pulls = get_pulls(owner,repo)
    pull_nums = []
    count = 0
    
    for pull in pulls:
        pull_nums.append(pull['issue_url'].split('/')[-1])
        count+=1
    
    if v: print ('\n%s pull numbers extracted.' % str(count))
    return pull_nums

        
def get_user_comments(owner,repo,pull,user):
    pull_comments = get_pull_comments(owner,repo,pull)
    user_comments = []
    count = 0
             
    for comment in pull_comments:
        login =  comment['user']['login']
        if login is user:
            user_comments.append(comment['body'])
            count +=1
            
    if v: print ('\n%s comments by %s in pull number %s' % str(count),user,pull)            
    return user_comments

