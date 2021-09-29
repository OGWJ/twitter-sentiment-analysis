from flask import Flask, request, jsonify
#from flask_cors import CORS
from textblob import TextBlob
import tweepy
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
#app.wsgi_app = QueryChecker(app.wsgi_app)


# GET sentiment for query TODAY
@app.route("/sentiment/<query>", methods=['GET'])
def sentiment_query(query):

    tweets = tweepy_controller.get_tweets(query)
    sentiment = tweepy_controller.get_sentiment(tweets)

    return str(sentiment)


# GET sentiment
@app.route("/sentiment/<query>/<n_days>", methods=['GET'])
def sentiment_query_n_days(query, n_days):

    if not n_days.isdigit():
        return 'Error: n_days must be an integer in the range 1 <= 7'

    n_days = int(n_days)

    if n_days > 7:
        return 'Error: n_days must be <= 7'

    dates = get_days_prior(n_days)
    data = []

    for date in dates:
        tweets = tweepy_controller.get_tweets(query, until=date)
        sentiment = tweepy_controller.get_sentiment(tweets)
        data.append((date, sentiment))

    return str(data)


@app.route("/future/<query>/<n_days>", methods=['GET'])
def future_query_n_days(query, n_days):

    n_days = int(n_days)
    dates = get_days_prior(n_days)
    data = []

    for date in dates:
        tweets = tweepy_controller.get_tweets(query, until=date)
        sentiment = tweepy_controller.get_sentiment(tweets)
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


# route should be passed existing data from db when






# Error handlling
@app.errorhandler(exceptions.NotFound)
def error_404():
    return jsonify({"message": 'valid routes are...'})

@app.errorhandler(exceptions.InternalServerError)
def error_500(err):
    return jsonify({"message": "Internal Server Error"})


# temporarily moved outside for testing file imports
config = dotenv_values('.env')
tweepy_controller = TwitterApiController(config)
predictive_model = model.Model(save=True, load=False)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
