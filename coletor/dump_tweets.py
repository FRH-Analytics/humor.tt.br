from pymongo import Connection
import conf
import sys

mongo_dbname=conf.MONGO_DBNAME
con = Connection()
db = con[mongo_dbname]
tweets_db = db['tweets']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dec']

if len(sys.argv) == 2:
  date_array = sys.argv[1].split('/')
  file_name = 'tweets_dump_' + date_array[2] + date_array[1] + date_array[0] + '.txt'
  tweets_file = open(file_name, 'w')
  tweets_file.write('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'
	.format('ID', 'USER','TEXT','DATE_TIME','LOCATION','TT'))

  date_pattern = '{} {} {}'.format(date_array[0],months[int(date_array[1])-1],date_array[2])
  for tweet in tweets_db.find({'created_at' : { '$regex' : '.*'+ date_pattern +'.*'} }):
    location = '' if not tweet.has_key('location') else tweet['location'].encode('utf-8')
    tweets_file.write('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'
	.format(tweet['id'], tweet['user']['screen_name'].encode('utf-8'), 
		tweet['text'].encode('utf-8'), tweet['created_at'],
		location, tweet['tt'].encode('utf-8') ))
  tweets_file.close()
else:
  print 'PLEASE tell me a date in the format DD/MM/YYYY!'
