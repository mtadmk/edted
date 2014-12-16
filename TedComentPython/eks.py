import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm


def talk_comments():
    query = "select talkid, count(id) from comments group by talkid"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (talkid, count) in cursor:
        tid.append(talkid)
        c.append(count)

    print 'komentarze do poszczegolnych talkow'
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(tid, c, color='g')
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('talk id')
    plt.title('komentarze do poszczegolnych talkow')
    plt.show(block=False)

    cursor.close()


def r_talk_comments():
    query = "select talkid, count(id) from comments group by talkid"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (talkid, count) in cursor:
        tid.append(talkid)
        c.append(count)

    global fig
    fig += 1
    plt.figure(fig)
    plt.hist(c, histtype='stepfilled', bins=20)
    # plt.yscale('log')
    plt.ylabel('ilosc talkow')
    plt.xlabel('liczba komentarzy')
    plt.title('rozklad komentarzy')

    cursor.close()


def talk_comments1():
    query = "select t.event_id, count(t.summ) from (select t.event_id, count(c.id) as summ from talks t join comments c on t.id = c.talkid group by c.id) t group by t.event_id"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (eventid, count) in cursor:
        tid.append(eventid)
        c.append(count)

    print 'komentarze do poszczegolnych eventow'
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(tid, c, color='r')
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('event id')
    plt.title('rozklad komentarzy do poszczegolnych eventow')
    plt.show(block=False)

    cursor.close()


def r_talk_comments1():
    query = "select t.event_id, count(t.summ) from (select t.event_id, count(c.id) as summ from talks t join comments c on t.id = c.talkid group by c.id) t group by t.event_id"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (eventid, count) in cursor:
        tid.append(eventid)
        c.append(count)

    print 'komentarze do poszczegolnych eventow'
    global fig
    fig += 1
    plt.figure(fig)
    plt.hist(c, histtype='stepfilled', bins=20)
    # plt.yscale('log')
    plt.ylabel('ilosc eventow')
    plt.xlabel('liczba komentarzy')
    plt.title('rozklad komentarzy')

    cursor.close()


def popular_themes_comments():
    query = "select count(t.id), th.name from (select talkid, count(id) num from comments group by talkid order by count(id) desc) c join talks t on c.talkid = t.id join theme_to_talk ttt  on t.id = ttt.talk_id  join themes th on th.id = ttt.theme_id  group by th.name order by count(t.id) desc"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (count, thname) in cursor:
        tid.append(thname)
        c.append(count)

    print 'komentarze do poszczegolnych motywow'
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(range(len(c)), c, color='y')
    plt.xticks(range(len(c)), tid, size='small', rotation='vertical', verticalalignment='bottom')
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('theme')
    plt.title('komentarze do poszczegolnych motywow')
    plt.show(block=False)

    cursor.close()


def popular_themes_number():
    query = "select th.name, count(ttt.talk_id) from theme_to_talk ttt join themes th on th.id = ttt.theme_id group by th.name order by count(ttt.talk_id) desc"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (thname, count) in cursor:
        tid.append(thname)
        c.append(count)

    desc = 'rozklad talkow do poszczegolnych motywow'
    print desc
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(range(len(c)), c, color='y')
    plt.xticks(range(len(c)), tid, size='small', rotation='vertical', verticalalignment='bottom')
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc talkow')
    plt.xlabel('theme')
    plt.title(desc)
    plt.show(block=False)


def time_comments():
    query = "select count(id), date_format(date_create, '%k') from comments group by date_format(date_create, '%k') order by convert(date_format(date_create, '%k'), unsigned integer)"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (count, thname) in cursor:
        tid.append(thname)
        c.append(count)

    desc = 'najpopularniejszy czas komentowania (godziny)'
    print desc
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(range(len(c)), c, color='y')
    plt.xticks(range(len(c)), tid, size='small', rotation='vertical')
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('czas')
    plt.title(desc)
    plt.show(block=False)
    cursor.close()


def time_day_comments():
    query = "select count(id), date_format(date_create, '%j') from comments group by date_format(date_create, '%j') order by convert(date_format(date_create, '%j'), unsigned integer)"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (count, thname) in cursor:
        tid.append(thname)
        c.append(count)

    cc = c[:]
    cc = sorted(cc)
    for x in cc[:5]:
        print tid[c.index(x)]

    desc = 'najpopularniejszy czas komentowania (dni)'
    print desc
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(range(len(c)), c, color='y')
    plt.xticks(range(len(c)), tid, size=6, rotation='vertical')
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('czas (dzien roku)')
    plt.title(desc)
    plt.show(block=False)
    cursor.close()


def t2():
    query = "select u.name, count(c.profile_id) from users u join comments c on c.profile_id = u.profile_id group by u.name order by count(c.profile_id) desc limit 5"
    cursor = cnx.cursor()

    cursor.execute(query)
    tid = []
    c = []
    for (thname, count) in cursor:
        tid.append(thname)
        c.append(count)

    cc = c[:]
    cc = sorted(cc)
    for x in cc[:5]:
        print tid[c.index(x)]

    desc = 'najpopularniejszy czas komentowania (dni)'
    print desc
    global fig
    fig += 1
    plt.figure(fig)
    plt.bar(range(len(c)), c, color='y')
    plt.xticks(range(len(c)), tid, size=6, rotation='vertical')
    # plt.subplot(2,1,1)
    plt.ylabel('ilosc komentarzy')
    plt.xlabel('czas (dzien roku)')
    plt.title(desc)
    plt.show(block=False)
    cursor.close()


def test1():
    # get talks ids
    query = "SELECT id from talks order by id limit 10"
    cursor = cnx.cursor()
    cursor.execute(query)
    tid = []
    c = []
    i = 1
    for t in cursor:
        tid.append(t[0])
    cursor.close()

    query = ("SELECT UNIX_TIMESTAMP(c.date_create) FROM talks t join comments c on c.talkid = t.id where t.id = %(emp_no)s order by UNIX_TIMESTAMP(c.date_create)")
    cursor = cnx.cursor()
    plots = []
    colors = cm.rainbow(np.linspace(0, 1, len(tid)))
    cid = 0
    for talkid in tid:
        cursor.execute(query, { 'emp_no': talkid})
        tid = []
        c = []
        i = 1
        for t in cursor:
            tid.append(t[0])
            c.append(i)
            i += 1
        plots.append(plt.plot(tid, c, color=colors[cid]))
        cid += 1

    plt.ylabel('ilosc komentarzy')
    plt.xlabel('czas')
    plt.title('wzrost komentarzy w czasie')
    plt.show()


config = {

    'user': 'root',
    'password': 'janosik',
    'host': 'localhost',
    'database': 'str2511_1',
    'raise_on_warnings': True,
}
cnx = mysql.connector.connect(**config)
fig = 1
# talk_comments1()
# talk_comments()
# popular_themes()
# popular_themes_number()
# popular_themes_comments()
# time_comments()
# time_day_comments()
t2()
plt.show()

#