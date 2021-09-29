from flask import Flask, request, jsonify
#from flask_cors import CORS
from textblob import TextBlob
#import tweepy
from dotenv import dotenv_values
from datetime import datetime, timedelta
import math
import numpy as np

from werkzeug import exceptions

import model
from middleware import QueryChecker
from controller import TwitterApiController
from date_utils import *

app = Flask(__name__)
#CORS(app)
app.wsgi_app = QueryChecker(app.wsgi_app)

twitter_api_controller = None
nlp = None


@app.route("/sentiment/<query>")
def sentiment_query(query):

    tweets = controller.get_tweets(query)
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


@app.errorhandler(exceptions.NotFound)
def error_404():
    return jsonify({"message": 'valid routes are...'})

@app.errorhandler(exceptions.InternalServerError)
def error_500(err):
    return jsonify({"message": "Internal Server Error"})


if __name__ == "__main__":
    config = dotenv_values('.env')
    controller = TwitterApiController(config)
    predictive_model = model.Model(save=True, load=False)
    app.run(debug=True, port=5000)
