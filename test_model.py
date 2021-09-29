import pytest
from unittest import mock
from model import Model
import numpy
from tensorflow.keras.models import Sequential, load_model

# init model for testing
model = Model()

# mock Keras functions
load_model = mock.MagicMock(name='load_model')

def test_init():
    assert model.history == None
    assert model.save == False
    return

#@patch(tesnroflow.keras.models) todo
def test_load():
    # model._load_model()
    # load_model.assert_called_once()
    # should call keras method
    # should return instance of keras model or expected
    #model = Model(load=False, save=False)
    #model.load()
    return

def test_load_fail():
    # mock invalid file
    # mock keras load_model func response?
    return

def test_save():
    # should call mocked keras model method 'save'
    return

def test_save_fail():
    # not sure how to test this
    return

def test_build():
    # should call mocked keras model, Sequential constructor
    # and compile
    return

def test_train():
    # should call mocked model.fit with mock args passed in func
    return

def test_train_fail():
    return

def test_predict():
    # should return a numpy float
    test_data = [7]
    pred = model.predict(test_data)
    assert type(pred[0, 0]) == numpy.float32
    return

# no point in testing this its not mine
def test_predict_fail():
    # should return error on
    #invalid_test_data = [2, 5]
    #with pytest.raises(RuntimeError) as excinfo:
        #model.predict(invalid_test_data)
    return
