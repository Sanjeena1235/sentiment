import pymysql
import time

import urllib
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

db = pymysql.connect(host="localhost", user="root", passwd="", db="minorproject")
cur = db.cursor()
def function1():
    cur.execute("select * from review")
    analyzer = SentimentIntensityAnalyzer()
    score = 0
    total = 0
    arr = []


    for i in cur.fetchall():
        vs = analyzer.polarity_scores(i[3])
        if vs['compound'] > 0:
            score = 1
            total = total + score
            sql = 'UPDATE review SET score=%s where id= %s'
            val = (score, i[0])
            cur.execute(sql, val)
        else:
            score = 0
            sql = 'UPDATE review SET score=%s where id= %s'
            val = (score, i[0])
            cur.execute(sql, val)

    arry = []
    cur.execute("select * from college")
    for i in cur.fetchall():
        arry.append(i[0])

    total=0
    cur.execute("select * from review")
    for i in cur.fetchall():
        total=total+i[4]

    if total==0:
        total=1



    cur.execute("select * from review")
    for i in arry:
        indscore = 0
        for j in cur.fetchall():
            if i == j[1]:# when id match add the score ie indscore
                indscore = indscore + j[4]
                x = (indscore / total) * 100
        vall = (x, i)
        sqql = " update college set score=%s where id=%s"
        cur.execute(sqql, vall)

    cur.execute("select * from college")
    for i in cur.fetchall():
        hitscore = 0
        hitscore = (i[10] / total) * 100
        sql = 'UPDATE college SET hitscore=%s where id= %s'
        val = (hitscore, i[0])
        cur.execute(sql, val)

    while True:
        cur.execute("select * from flag")
        for i in cur.fetchall():
            if i[1] == 1:
                function1()
                sql = "update flag set value=%s where id=%s"
                a = 0
                val = (a, i[0])
                cur.execute(sql, val)
                time.sleep(5)

cur.close()
db.close()





