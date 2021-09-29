from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras import Input


class Model:

    def __init__(self, load=False, save=False):
        self.history = None
        self.save = save

        if load:
            self.model = self._load_model()
            # self.model.load_weights('model.h5')

        else:
            self.model = self._build()


    def __repr__(self):
        return 'Linear DNN'


    def _load_model(self):
        print('* loading model...')
        model = load_model('model.h5')
        print('\rfinished loading model')
        return model


    def _save(self):
        print('* saving model...')
        self.model.save('model.h5')
        print('\rfinished saving model')
        return


    def _build(self):
        print('* building model...')
        model = Sequential([
            Input(shape=(1,), name='input'),
            Dense(32, activation='relu', name='dense_1'),
            Dense(32, activation='relu', name='dense_2'),
            Dense(32, activation='relu', name='dense_3'),
            Dense(1, name='prediction')
        ])
        model.compile(loss='mean_absolute_error', optimizer='adam')
        print('\rfinished building model')
        return model


    def _train(self, x, y):
        print('* training model...')
        self.history = self.model.fit(x, y, epochs=500)
        if self.save:
            self._save()
        print('\rfinsihed training model')
        return


    def predict(self, d):
        return self.model.predict(d)
