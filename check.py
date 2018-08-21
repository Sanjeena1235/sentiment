import pymysql

import urllib
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

db=pymysql.connect(host="localhost",user="root",passwd="",db="minorproject")
cur=db.cursor()
cur.execute("select * from review")
analyzer = SentimentIntensityAnalyzer()


arr = []
total=0
#code for analysis
threshold = 0.20000
x=0
for i in cur.fetchall():
    vs = analyzer.polarity_scores(i[3])
    print(vs['compound'])

    #if vs['compound'] >= threshold or vs['compound'] <= -threshold:
    if vs['compound']>= 0.00000000:
        score=1
        total = total+score
        sql = 'UPDATE review SET score=%s where id= %s'
        print('ghdhdhdhd')
        val = (score, i[0])
        cur.execute(sql, val)
    else:
        score = 0
        sql = 'UPDATE review SET score=%s where id= %s'
        print("sucess")
        val = (score, i[0])
        cur.execute(sql, val)

cur.execute("select * from review")
for i in cur.fetchall():
    print(i[4])

cur.close()
db.close()
