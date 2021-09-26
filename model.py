from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

    # TODO:
    # check for existing model
    # else build new model

class Model:
    def __init__(self):
        self.model = self._build()
        self.history = None

    def __repr__(self):
        return 'Linear DNN'
    
    def predict(self, d):
        return self.model.predict(d)

    def _build(self):
        model = Sequential()
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_absolute_error', optimizer='adam')
        return model
    
    def _train(self, x, y):
        self.history = self.model.fit(x, y, epochs=500)
        return

    def evaluate(self, df):
        return