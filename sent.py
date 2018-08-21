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

    # code for analysis
    threshold = 0.6

    for i in cur.fetchall():
        vs = analyzer.polarity_scores(i[3])
        if vs['compound'] >= threshold or vs['compound'] <= -threshold:
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
        arr.append(i[1])
    # extracting unique ids from arr...arr contains list of college ids
    b = set(arr)
    arry = []
    for i in b:
        arry.append(i)

    for i in arry:  # counting no of appearance
        sum = 0
        for j in arr:
            if i == j:
                sum = sum + 1
        # bias gives total no of review
        sql = 'UPDATE college SET bias=%s where id= %s'
        sqql = 'UPDATE score SET totalreview=%s where id= %s'
        val = (sum, i)
        cur.execute(sql, val)
        cur.execute(sqql, val)

    cur.execute("select * from review")
    for i in arry:
        x = 0
        indscore = 0
        for j in cur.fetchall():
            if i == j[1]:  # when id match add the score ie indscore
                indscore = indscore + j[4]
        x = (indscore / total) * 100
        val = (indscore, j[1])
        vall = (x, j[1])
        sql = " update score set posreview=%s  where id=%s"
        sqql = " update college set biases=%s where id=%s"
        cur.execute(sqql, vall)
        cur.execute(sql, val)
        # cur.execute(" update score set posreview=indscore  where id='print(j[1])'")
        # cur.execute(" update college set biases=x  where id='print(j[1])'")

    cur.execute("select * from college")
    for j in cur.fetchall():
        scores = 1
        if j[8] == 0:
            scores = (j[9] / 1)
        else:
            scores = (j[9] / j[8])
        val = (scores, j[0])
        sql = "update college set score=%s where id=%s"
        sqql = "update score set score=%s where id=%s"
        cur.execute(sql, val)
        cur.execute(sqql, val)
        # cur.execute("update college set score=scores where id='print(j[0])']")
        # cur.execute("update score set score=scores where id='print(j[0])'")

    cur.execute("select * from score")
    negrev = []
    for j in cur.fetchall():
        x = j[5] - j[2]
        sql = "update score set negreview=%s where id=%s"
        val = (x, j[1])
        cur.execute(sql, val)
    # calculation of hit score
    cur.execute("select * from college")
    total = 0
    for i in cur.fetchall():
        total = total + i[10]

    cur.execute("select * from college")
    for i in cur.fetchall():
        hitscore = 0
        hitscore = (i[10] / total) * 100
        sql = 'UPDATE college SET hitscore=%s where id= %s'
        val = (hitscore, i[0])
        cur.execute(sql, val)
    cur.execute("select * from college")
    for i in cur.fetchall():
        print(i[7])
        print(i[8])
        print(i[9])
        print(i[10])



while True:
    cur.execute("select * from flag")
    for i in cur.fetchall():
        if i[1] == 1:
            function1()
            time.sleep(20)
            print("sucessess")
            sql = "update flag set value=%s where id=%s"
            a = 0
            val = (a, i[0])
            cur.execute(sql, val)


# cur.execute("select * from flag")
# for i in cur.fetchall():
#     print(i[1])
cur.close()
db.close()
