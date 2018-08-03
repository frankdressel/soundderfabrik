import ly.music
import numpy
import keras
from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM
from keras.engine.topology import Layer
from keras import backend as K

import notemodel

class MyLayer(Layer):

    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(MyLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # Create a trainable weight variable for this layer.
        self.kernel = self.add_weight(name='kernel',
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='uniform',
                                      trainable=True)
        super(MyLayer, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        print(x)
        y=x[:,:]
        return K.dot(x, self.kernel)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

doc = ly.document.Document.load('allemeineentchen.ly')
d = ly.music.document(doc)

relatives = [r for r in d.find(ly.music.items.Relative)]

# The denominator taken into account for a note length here.
min_length = 8

# There is just 1 relative, but nevertheless use a loop here.
for rel in relatives:
    elements = [n for n in rel.find((ly.music.items.Note, ly.music.items.Rest))]

    notes = []

    # It looks like the first element of a relative defines the pitch and can be skipped.
    for elem in elements[1:]:
        if type(elem) == ly.music.items.Note:
            notes.append(elem.pitch.output())
            for i in range(1, min_length//elem.length().denominator):
                notes.append("cont")
        if type(elem) == ly.music.items.Rest:
            notes.append("Rest")
            for i in range(0, min_length//elem.length().denominator):
                notes.append("cont")

num_timesteps=10

nm=notemodel.Model(notes)

input_x, input_y=nm.create_input_output(notes, num_timesteps, min_length)

num_features=input_y.shape[1]
num_classes=input_y.shape[1]

model=Sequential()
model.add(LSTM(num_features+1, input_shape=(num_timesteps, num_features+1), return_sequences=True))
model.add(LSTM(num_features+1))
#model.add(MyLayer(num_features+1))
model.add(Dense(num_classes))
model.add(Activation("softmax"))


def createTestInput():
    translated = translation["cont"]
    onehot = numpy.zeros((5, 9))

    for i in range(5):
        onehot[i, translated]=1
        onehot[i, -1]=i

    return K.variable(K.cast_to_floatx(numpy.tile(onehot, [1, 5, 1])))

def createTestOutput():
    translated = translation["cont"]
    onehot = numpy.zeros((5, 8))

    for i in range(5):
        onehot[i, translated] = 1

    return K.variable(K.cast_to_floatx(numpy.tile(onehot, [5, 1])))

#test_input=createTestInput()
#test_function=notemodel.Model().loss(test_input)

#test_result=test_function(createTestOutput(), createTestOutput())
#print(K.eval(test_result))




#model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
model.compile(loss=nm.loss(model.input), optimizer="adam", metrics=['accuracy'])

model.fit(input_x, input_y, epochs=1000, batch_size=10)

stride=notes[len(notes)-num_timesteps:]
#stride=notes[0:num_timesteps]
for i in range(20):
    input_x=[]
    translated = [translation[s] for s in stride]
    onehot = numpy.zeros((len(stride), num_features+1))
    onehot[numpy.arange(len(stride)), translated] = 1

    for j in range(num_timesteps):
        index_in_measure = (i + j + len(notes) - num_timesteps) % min_length
        onehot[j][num_features]=index_in_measure
    input_x.append(onehot)

    prediction=model.predict(numpy.array(input_x))
    sorted_prediction=numpy.argsort(-prediction[0])

    next_note=""
    #if index_in_measure==0 and reverse_translation[numpy.argmax(prediction)]=="cont":
    #    next_note=reverse_translation[sorted_prediction[1]]
    #else:
    #    next_note=reverse_translation[sorted_prediction[0]]
    next_note = reverse_translation[sorted_prediction[0]]

    #next_note = reverse_translation[numpy.argmax(prediction)]
    print(next_note)

    stride=stride[1:]
    stride.append(next_note)

