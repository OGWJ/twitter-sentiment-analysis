from flask import Flask
from textblob import TextBlob
import tweepy
from dotenv import dotenv_values


app = Flask(__name__)
twitter_api_controller = None
nlp = None


class Twitter_API_Controller:
    
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

    def get_tweets(self, query, count=10):
        tweets = tweepy.Cursor(self.api.search,
        q=query,
        lang='en').items(5)
        return tweets
    

def get_sentiment(tweets):

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


@app.route("/<query>")
def index(query):

    print('getting tweets containing \'{}\'\n'.format(query))
    tweets = twitter_api_controller.get_tweets(query)
    sentiment = get_sentiment(tweets)

    return str(sentiment)


if __name__ == "__main__":
    config = dotenv_values('.env')
    twitter_api_controller = Twitter_API_Controller(config)
    app.run(debug=True, port=5000)
