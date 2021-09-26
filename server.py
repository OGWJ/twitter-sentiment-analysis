from flask import Flask
from textblob import TextBlob
import tweepy
from dotenv import dotenv_values
from datetime import datetime, timedelta


app = Flask(__name__)
twitter_api_controller = None
nlp = None

today = datetime.today().strftime('%Y-%m-%d')

def valid_date(date):
    return True

def within_seven_days(start, end):
    return True

def get_days_prior(n_days):
    dates = [today]
    for i in range(n_days):
        current_day = dates[i]
        yyyy, mm, dd = current_day.split('-')
        current_day = datetime(int(yyyy), int(mm), int(dd))
        previous_day = current_day - timedelta(1)
        dates.append(previous_day.strftime('%Y-%m-%d'))

    return sorted(dates)


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

    def get_tweets(self, query, count=1, 
                   since=today,
                   until=today):

        tweets = tweepy.Cursor(self.api.search,
        q=query,
        # since=since,
        until=until,
        result_type='recent',
        lang='en').items(count)
        return tweets


def get_sentiment(tweets):

    avg_sentiment_polarity = 0
    n_tweets = 0

    for tweet in tweets:

        print(f'\n{tweet.created_at}\n{tweet.text}')

        blob = TextBlob(tweet.text)
        tweet_sentiment = 0
        n_tweets += 1

        for sentence in blob.sentences:
            tweet_sentiment += sentence.sentiment.polarity

            tweet_sentiment /= len(blob.sentences)
            avg_sentiment_polarity += tweet_sentiment

    return avg_sentiment_polarity / n_tweets



# GET today default count is 10
@app.route("/<query>")
def index_query(query):

    tweets = twitter_api_controller.get_tweets(query) 
    sentiment = get_sentiment(tweets)

    return str(sentiment)


# GET past 7 days
@app.route("/<query>/<n_days>")
def index_query_n_days(query, n_days):

    n_days = int(n_days)

    if n_days > 7:
        return 'Error: days prior must be <= 7'

    dates = get_days_prior(n_days)
    data = []

    for date in dates:
        tweets = twitter_api_controller.get_tweets(query, until=date)
        sentiment = get_sentiment(tweets)
        data.append((date, sentiment))

    return str(data)


if __name__ == "__main__":
    config = dotenv_values('.env')
    twitter_api_controller = Twitter_API_Controller(config)
    app.run(debug=True, port=5000)
