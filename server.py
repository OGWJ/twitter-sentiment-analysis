from flask import Flask
from textblob import TextBlob
import tweepy
from dotenv import dotenv_values
from datetime import datetime, timedelta
import math
import numpy as np

import model

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
                   until=today):

        tweets = tweepy.Cursor(self.api.search,
        q=query,
        until=until,
        result_type='recent',
        lang='en').items(count)
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


@app.route("/sentiment/<query>")
def sentiment_query(query):

    tweets = twitter_api_controller.get_tweets(query) 
    sentiment = get_sentiment(tweets)

    return str(sentiment)


@app.route("/sentiment/<query>/<n_days>")
def sentiment_query_n_days(query, n_days):

    if not n_days.isdigit():
        return 'Error: n_days must be an integer in the range 1 <= 7'

    n_days = int(n_days)

    if n_days > 7:
        return 'Error: n_days must be <= 7'

    dates = get_days_prior(n_days)
    data = []

    for date in dates:
        tweets = twitter_api_controller.get_tweets(query, until=date)
        sentiment = get_sentiment(tweets)
        data.append((date, sentiment))

    return str(data)


def format_date(date):
    return date.strftime('%Y-%m-%d')


def get_future_dates(n_days):
    yyyy, mm, dd = today.split('-')
    tomorrow = datetime(int(yyyy), int(mm), int(dd)) + timedelta(1)
    dates = [tomorrow]
    for i in range(n_days - 1):
        next_day = dates[i] + timedelta(1)
        dates.append(next_day)
    
    return [format_date(date) for date in dates]


@app.route("/future/<query>/<n_days>")
def future_query_n_days(query, n_days):

    n_days = int(n_days)
    dates = get_days_prior(n_days)
    data = []

    for date in dates:
        tweets = twitter_api_controller.get_tweets(query, until=date)
        sentiment = get_sentiment(tweets)
        data.append((date, sentiment))

    x = np.array([i for i in range(n_days + 1)])
    y = np.array([sentiment for _, sentiment in data])
    predictions = []

    predictive_model._train(x, y)

    for i in range(n_days):

        prediction = predictive_model.predict(np.array([n_days + i]))
        predictions.append(float(prediction[0]))

    future_dates = get_future_dates(n_days)
    dates.append([date for date in future_dates])

    future_data = list(zip([date for date in future_dates], predictions))
    for i in range(len(future_data)):
        data.append(future_data[i])
    
    return str(data)


if __name__ == "__main__":
    config = dotenv_values('.env')
    twitter_api_controller = Twitter_API_Controller(config)
    predictive_model = model.Model()
    app.run(debug=True, port=5000)
