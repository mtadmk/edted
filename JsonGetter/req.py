import requests
import sys

headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive' ,'Accept': 'application/json, text/javascript'}
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    r = requests.get('http://www.ted.com/conversation_forums/'+str(i)+'?page=1&per_page=9000', headers=headers)
    if r.status_code in [200, 201] and r.text != 'null':
        with open(str(i)+'.json', 'w') as f:
            f.write(r.text.encode('utf8'))
            print 'discussion ' + str(i) + ' saved'
    else:
        print str(i) + ' not exisits'
