import csv
import mysql.connector
import pickle
import matplotlib.pyplot as plt
import numpy as np
import difflib
import matplotlib.cm as cm
from collections import defaultdict, Counter
import operator


def t2():
    query = "select u.profile_id, u.profile_score, us.c from users u join (select profile_id, count(comment) c from comments group by profile_id having count(comment) between 30 and 1000 order by count(comment)) us on u.profile_id = us.profile_id where u.profile_score between 100 and 4000"
    cursor = cnx.cursor()

    cursor.execute(query)
    uid = []
    score = []
    c = []
    for (id, sc, count) in cursor:
        uid.append(id)
        score.append(sc)
        c.append(count)

    desc = 'stosunek ilosci komentarzy profilu uzytkownika do jego ilosci punktow'
    print desc
    global fig
    fig += 1
    plt.figure(fig)
    plt.scatter(score, c)
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('wynik uzytkownika')
    plt.title(desc)
    plt.show(block=False)
    cursor.close()


def t21():
    query = "select c.profile_id, c.id commentid, n.nlpword from comments c join nlp n on c.id = n.commentid group by c.profile_id having count(c.profile_id) > 5"
    # query = " select c.profile_id, c.id commentid, n.nlpword from comments c join nlp n on c.id = n.commentid"
    cursor = cnx.cursor()

    loadnew = True
    if not loadnew:
        load = True
        if not load:
            cursor.execute(query)
            # uid = []
            # cid = []
            # words = []
            dict = {}
            i = 0
            for (id, cid, word) in cursor:
                if id not in dict:
                    dict[id] = {}
                innerdict = dict[id]
                if cid not in innerdict:
                    innerdict[cid] = []
                innerdict[cid].append(word)
                # i+=1
                # if i == 15:
                # break
            output = open('icw.pkl', 'wb')
            pickle.dump(dict, output)
        else:
            pkl_file = open('icw.pkl', 'rb')
            dict = pickle.load(pkl_file)

        newdict = {}
        for k, v in dict.iteritems():
            newdict[k] = []
            for cid, words in v.iteritems():
                newdict[k].extend(words)

        for k, v in newdict.iteritems():
            newdict[k] = sorted(Counter(v).items(), key=operator.itemgetter(1))

        output = open('newdict.pkl', 'wb')
        pickle.dump(newdict, output)
    else:
        pkl_file = open('newdict.pkl', 'rb')
        newdict = pickle.load(pkl_file)

    print 'enddddddddddddddddddddddddddddddddddd load'
    for k, v in newdict.iteritems():
        newdict[k] = []
        for word, count in v:
            # if count > 1:
            newdict[k].append(word)
    print 'check1'
    with open('eggs.csv', 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        ignore = []
        print 'check2'
        for k, v in newdict.iteritems():
            for k1, v1 in newdict.iteritems():
                if v1 not in ignore:
                    sm = difflib.SequenceMatcher(None, v, v1)
                    rat = sm.ratio()
                    if 0.66 < rat < 1.:
                        wr.writerow([k, k1, "{0:.2f}".format(rat)])
                        # print k, k1, rat
            csvfile.flush()
            ignore.append(v)


#
config = {

    'user': 'root',
    'password': 'janosik',
    'host': 'localhost',
    'database': 'ed0112',
    'raise_on_warnings': False,
}
cnx = mysql.connector.connect(**config)
fig = 1
t21()
plt.show()

#