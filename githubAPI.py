import requests
import json
import pprint    
    
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
    
    print ('\n%s open pull requests.' % str(count))
    return pulls


#get the first 100 of the open pull requests for a repo, and return the issue urls
def get_pull_nums(owner,repo):
    #/repos/:owner/:repo/pulls
    count = 0
    pull_nums = []
    
    request = requests.get('https://api.github.com/repos/%s/%s/pulls?per_page=100' % owner, repo)
    content = json.loads(request.content)
    
    for pull in content:
        pull_nums.append(pull['issue_url'].split('/')[-1])
        count+=1
    
    print ('\n%s open pull requests with issue URLs.' % str(count))
    return pull_nums


#get all the comments from a specific user    
def get_comments(owner,repo,user):
    #/repos/:owner/:repo/issues/:number/comments
    pull_nums = get_pull_nums(owner,repo)
    count = 0
    comments = []
    
    for num in pull_nums:
        request = requests.get('https://api.github.com/repos/%s/%s/issues/%s/comments' % owner, repo, num)
        content = json.loads(request.content)

        for comment in content:
            login =  comment['user']['login']
            if login is user:
                comments.append(comment['body'])
                count +=1
 
    print ('\n%s comments by %s' % str(count), user)
    return comments
