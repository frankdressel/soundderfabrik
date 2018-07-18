import numpy

from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed

num_batches=10
num_timesteps=2
num_features=3

num_classes=3

input_x=numpy.zeros((num_batches, num_timesteps, num_features))
# Categorical prediction: A class label
input_y=numpy.random.random((num_batches, num_classes))

model=Sequential()
# If another layer of LSTM is used, return_sequences must be True
model.add(LSTM(num_features, input_shape=(num_timesteps, num_features)))
model.add(Dense(num_classes))

model.compile(loss='categorical_crossentropy', optimizer="adagrad")

model.fit(input_x, input_y)