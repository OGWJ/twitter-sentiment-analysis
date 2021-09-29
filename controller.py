from date_utils import today
import tweepy
from textblob import TextBlob

class TwitterApiController:

    def __init__(self, config):
        self.consumer_key = config['CONSUMER_KEY']
        self.consumer_secret = config['CONSUMER_SECRET']
        self.access_token = config['ACCESS_TOKEN']
        self.access_secret= config['ACCESS_SECRET']
        self.api = self.init_tweepy();


    def init_tweepy(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        return tweepy.API(auth)


    def get_tweets(self, query, count=1,
                   until=today):

        tweets = tweepy.Cursor(self.api.search,
        q=query,
        until=until,
        result_type='recent',
        lang='en').items(count)
        return tweets


    def get_sentiment(self, tweets):

        avg_sentiment_polarity = 0
        n_tweets = 0

        for tweet in tweets:

            blob = TextBlob(tweet.text)
            tweet_sentiment = 0
            n_tweets += 1

            for sentence in blob.sentences:
                tweet_sentiment += sentence.sentiment.polarity

                tweet_sentiment /= len(blob.sentences)
                avg_sentiment_polarity += tweet_sentiment

        return avg_sentiment_polarity / n_tweets


