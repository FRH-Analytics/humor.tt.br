import twitter
import conf

tw_consumer_key=conf.TWITTER_CONSUMER_KEY
tw_consumer_secret=conf.TWITTER_CONSUMER_SECRET
tw_access_token_key=conf.TWITTER_ACCESS_TOKEN_KEY
tw_access_token_secret=conf.TWITTER_ACCESS_TOKEN_SECRET
monitored_place_woeid=conf.MONITORED_PLACE_WOEID
monitored_place_geocode=conf.MONITORED_PLACE_GEOCODE
monitored_place_lang=conf.MONITORED_PLACE_LANG
mongo_dbname=conf.MONGO_DBNAME

temp_geocode=monitored_place_geocode.split(',')
monitored_place_geocode=(temp_geocode[0],temp_geocode[1],temp_geocode[2])

api=twitter.Api(consumer_key=tw_consumer_key,consumer_secret=tw_consumer_secret,
                access_token_key=tw_access_token_key,access_token_secret=tw_access_token_secret,cache=None)

#GET current trend topics for a place!
url_placed_trends = 'https://api.twitter.com/1.1/trends/place.json?id={}'.format(monitored_place_woeid)
json = api._FetchUrl(url_placed_trends)
trends = api._ParseAndCheckTwitter(json)
place_trends = []
for t in trends[0]['trends']:
    place_trends.append(twitter.Trend(name=t['name'],query=t['query'],timestamp=trends[0]['created_at']))

#GET Tweets by trend
trend_tweets = []
for topic in place_trends:
    print '=========', topic.query
    for page in range(1,10):
        print page
        try: #Some crazy error happend once
            tweets = api.GetSearch(term=topic.query,per_page=100,page=page,geocode=monitored_place_geocode,lang=monitored_place_lang)
        except:
            tweets = []
        for t in tweets:
            t_dict = t.AsDict()
            t_dict['tt'] = topic.name
            trend_tweets.append(t_dict)
        if len(tweets) < 100: break

#Saving everything

def to_dict(tt, att_list):
    dict_to_return = {}
    for att in att_list:
        dict_to_return[att] = tt.__dict__[att]
    return dict_to_return
    
from pymongo import Connection
con = Connection()
db = con[mongo_dbname]

##TRENDS
trends_db = db['trends']
attribs = ['name', 'query', 'timestamp']
for t in place_trends:
    trends_db.insert(to_dict(t, attribs))

##TWEETS
tweets_db = db['tweets']
for t in trend_tweets:
    tweets_db.insert(t)
