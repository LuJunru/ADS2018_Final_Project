import tweepy
import json
import datetime

timetag = str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour)
geo_tweets = {}
geo_tweets_id = set()
    
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.coordinates is not None and status.id not in geo_tweets_id:
            geo_tweets[status.id] = {"coordinates":status.coordinates, "text":status.text, "time":str(status.created_at)}
            geo_tweets_id.add(status.id)
        if len(geo_tweets) % 500 == 0:
            print(len(geo_tweets))
            with open('%s_%s.json'%(timetag, len(geo_tweets)), 'w') as outfile:
                json.dump(geo_tweets, outfile)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

consumer_key = "your own consumer key"
consumer_secret = "your own consumer secret"
access_token = "your own access token"
access_token_secret = "your own access token secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
while True:
    try:
        stream.filter(locations=[-74,40,-73,41], stall_warnings=True)
    except:
        print("Some error occured.")
        pass
