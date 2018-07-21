from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM

class SimpleCategoricalLSTM():
    def __init__(self):
        pass

    def fit(self, testdata):
        input_x, input_y=testdata

        num_timesteps=input_x.shape[1]
        num_features=input_x.shape[2]
        num_classes=len(input_y[0])

        model=Sequential()
        # If another layer of LSTM is used, return_sequences must be True
        model.add(LSTM(num_features, input_shape=(num_timesteps, num_features), return_sequences=True))
        model.add(LSTM(num_features))
        model.add(Dense(num_classes))
        model.add(Activation("softmax"))

        model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])

        model.fit(input_x, input_y, epochs=200, batch_size=10)

        return model.predict(input_x)