from os import listdir, path
from os.path import isfile, join
import datetime
import json
import mysql.connector
import re
import sys


def handle_obj(obj, talkid):
    threadid = handle_thread(obj, talkid)
    comments = obj['discussion_thread']['thread'][0]
    for key, comment in comments.iteritems():
        handle_comment(comment, threadid)


comment_table = 'comments'


def handle_comment(comment, threadid):
    children = comment['children']
    if children:
        for childkey, childcomment in children.iteritems():
            handle_comment(childcomment, threadid)

    add_comment = ('insert into ' + comment_table +
                   ' (id, threadid, comment, date_create, date_activity, deleted, deleted_reason, discussion_id, '
                   'expired, level, name, parent_id, profile_id, profile_score, replies, score, user_id)'
                   'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )')
    try:
        vals = [comment[v] for v in
                ('comment_id', 'comment', 'date', 'date_activity', 'deleted', 'deleted_reason', 'discussion_id', ''
                                                                                                                 'expired',
                 'level', 'name', 'parent_id', 'profile_id', 'profile_score', 'replies', 'score', 'user_id')]

        vals.insert(1, int(threadid))
        vals[3] = datetime.datetime.fromtimestamp(long(vals[3])).strftime('%Y-%m-%d %H:%M:%S.%f')
        vals[4] = datetime.datetime.fromtimestamp(long(vals[4])).strftime('%Y-%m-%d %H:%M:%S.%f')
        for i, n in enumerate(vals):
            if isinstance(n, basestring):
                vals[i] = n.encode('ascii', 'ignore').decode('ascii')

        cursor.execute(add_comment, vals)
        cnx.commit()
    except KeyError:
        print 'comment error', comment


thread_table = "threads"

# add talkid in second insert
def handle_thread(thread, talkid):
    add_thread = ('insert into ' + thread_table +
                  ' (id, talk_id, comments_count, conv_id, conv_type, vote_count, flag_count)'
                  'values (%s, %s, %s, %s, %s, %s, %s)')
    vals = [thread[v] for v in
            ('id', 'comment_count', 'conversation_id', 'conversation_type', 'vote_count', 'flag_count')]
    vals.insert(1, int(talkid))

    cursor.execute(add_thread, vals)
    cnx.commit()
    return thread['id']


config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'ed',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

cursor.execute('drop table threads')
cursor.execute(' drop table comments')
cursor.execute(
    'create table threads (id int, talk_id int, comments_count int, conv_id int, conv_type varchar(100), flag_count int, vote_count int)')
cursor.execute(
    'create table comments (id int, threadid int, comment varchar(20000), date_create datetime, date_activity datetime, deleted bool, deleted_reason varchar(1000), discussion_id int, expired bool, level int, name varchar(100), parent_id int, profile_id int, profile_score int, replies int, score int, user_id int)')
json_files = [f for f in listdir('jsons') if isfile(join('jsons', f)) and path.splitext(f)[1] == '.json']
#json_files = ['id_1386_no_11324.json']
for json_file in json_files:
    with open('jsons/' + json_file, 'r') as f:
        print 'handling ' + f.name
        obj = json.loads(f.read().replace('\n', ''))
        talkid = re.search(r'\d+', json_file).group()
        handle_obj(obj, talkid)
