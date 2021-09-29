import pytest
from server import sentiment_query, sentiment_query_n_days

# Endpoint Tests
#@pytest.mark. # ... [('query', 'n_days')]
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
