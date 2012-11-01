from pymongo import Connection
con = Connection()
db = con['Analytics_Tweets']
trends_db = db['trends']
tweets_db = db['tweets'] 
print 'trends= ', trends_db.count()
print 'tweets= ', tweets_db.count()
