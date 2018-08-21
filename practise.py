
import pymysql

import urllib
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

db=pymysql.connect(host="localhost",user="root",passwd="",db="minorproject")
cur=db.cursor()
cur.execute("select * from review")
analyzer = SentimentIntensityAnalyzer()
scores= 0
total = 0
arr = []

#code for analysis
threshold = 0.6

for i in cur.fetchall():
    vs = analyzer.polarity_scores(i[3])
    if vs['compound'] >= threshold or vs['compound'] <= -threshold:
        if vs['compound'] > 0:
            scores=1
            total = total+scores
            sql = 'UPDATE review SET score=%s where id= %s'
            val = (scores, i[1])
            cur.execute(sql, val)
    else:
            scores=1
            sql = 'UPDATE review SET score=%s where id= %s'
            val = (scores, i[1])
            cur.execute(sql, val)
a=0
cur.execute("select * from review")
for i in cur.fetchall():
    print(i[4])
    a=a+1
print(a)

