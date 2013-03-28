from libsaas.services import github
import configuration
import requests
import json
import pprint    
    
pp = pprint.PrettyPrinter(indent=4)

def get_pull_nums():
    #/repos/:owner/:repo/pulls
    request = requests.get('https://api.github.com/repos/bitcoin/bitcoin/pulls?per_page=100')
    count = 0
    pulls_nums = []
    
    content = json.loads(request.content)
    
    for pull in content:
        pulls.append(pull['issue_url'].split('/'))
        count+=1
    
    
cc=0
bc =0




#/repos/:owner/:repo/issues/:number/comments
r2 = requests.get('https://api.github.com/repos/bitcoin/bitcoin/issues/2415/comments') 
j2 = json.loads(r2.content)

for item2 in j2:
    cc+=1
    user = item2['user']['login']
    if user.count('BitcoinPullTester') > 0:
        bc+=1
        print item2['body']

print 'pulls: ' + str(pc)    
print 'comments: ' + str(cc)
print 'binaries: ' + str(bc)
print 'done'



