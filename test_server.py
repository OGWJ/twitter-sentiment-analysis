import pytest
from unittest import mock
from server import app, sentiment_query, sentiment_query_n_days, tweepy_controller


# Mock model and controller methods
tweepy_controller.get_tweets = mock.MagicMock(name='get_tweets')
tweepy_controller.get_sentiment = mock.MagicMock(name='get_sentiment')


# Endpoint Tests
tweepy_controller.get_sentiment.return_value = 5
test_cases = [('test', '5')]
@pytest.mark.parametrize('query, expected', test_cases)
def test_sentiment_query_good_paths(query, expected):
    retval = sentiment_query(query)
    tweepy_controller.get_tweets.assert_called_once_with(query)
    tweepy_controller.get_sentiment.assert_called_once()
    assert retval == expected


# todo mock return value for failed tweepy controller methods
test_cases = [('^test', '5')]
@pytest.mark.parametrize('query, expected', test_cases)
def test_sentiment_query_bad_paths(query, expected):
    return















#def test_future_query_good_paths(query, n_days, expected):
#    assert future_query_n_days(query, n_days).status == 200

# @pytest.mark... [('$%#@!\/', 7, 'Error: ...')]
#def test_future_query_bad_paths(query, n_days, expected_error):
#    assert test_future_query_bad_paths(query, n_days) == expected_error




# Unit Tests
def test_path_calls_controller():
    #retval = sentiment_query('test')
    #assert type(retval) == string
    return

def test_path_does_not_call_controller():
    return

def test_path_calls_model():
    return

def test_path_does_not_call_model():
    return

def test_server_initialises_model():
    return

def test_server_initialises_controller():
    return
