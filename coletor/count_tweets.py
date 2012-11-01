from pymongo import Connection
import conf

mongo_dbname=conf.MONGO_DBNAME

con = Connection()
db = con[mongo_dbname]

trends_db = db['trends']
tweets_db = db['tweets'] 

print 'trends= ', trends_db.count()
print 'tweets= ', tweets_db.count()
