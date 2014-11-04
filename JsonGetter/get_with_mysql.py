import mysql.connector
import requests
import re


def get_json(id, number):
    headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive',
               'Accept': 'application/json, text/javascript'}
    r = requests.get('http://www.ted.com/conversation_forums/' + number + '?page=1&per_page=9000', headers=headers)
    if r.status_code in [200, 201] and r.text != 'null':
        with open('id_'+str(id)+'_no_'+number + '.json', 'w') as f:
            f.write(r.text.encode('utf8'))
            print 'discussion ' + number + ' saved'
    else:
        print number + ' not exisits'


config = {
    'user': 'root',
    'password': 'xxx',
    'host': '127.0.0.1',
    'database': 'ed',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

query = ("select id, slug from talks")
cursor.execute(query)

headers = {'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive'
}

thread_id = 'threadId'

for (id, slug) in cursor:
    r = requests.get('http://www.ted.com/talks/' + slug, headers=headers)
    if r.status_code in [200, 201] and r.text != 'null':
        for line in r.text.split("\n"):
            if thread_id in line:
                part = line.split(thread_id, 1)[1]
                number = re.search(r'\d+', part).group()
                get_json(id, number)
cnx.close()

