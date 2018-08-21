import pymysql

import urllib
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

db=pymysql.connect(host="localhost",user="root",passwd="",db="minorproject")
cur=db.cursor()
cur.execute("select * from college")
total=0
for i in cur.fetchall():
    total=total+i[10]
print(total)
cur.execute("select * from college")
for i in cur.fetchall():
    hitscore=0
    hitscore=(i[10]/total)*100
    sql = 'UPDATE college SET hitscore=%s where id= %s'
    val=(hitscore,i[0])
    cur.execute(sql, val)
cur.execute("select * from college")
for i in cur.fetchall():
    print(i[12])
