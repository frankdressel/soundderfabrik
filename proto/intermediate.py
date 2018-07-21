# coding: utf-8
import fractions
from builtins import input

import numpy
import sklearn.pipeline
import sklearn.preprocessing
import ly.music
from keras import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM


doc = ly.document.Document.load('/home/vagrant/Downloads/Sheep.ly')
d = ly.music.document(doc)


def measures(notes):
    summedLength=fractions.Fraction(0, 1)
    notesInMeasure=[]
    for note in notes:
        summedLength=summedLength+note['length']
        notesInMeasure.append(note)
        if summedLength==1:
            summedLength=0
            result=[n for n in notesInMeasure]
            notesInMeasure=[]
            yield result


relatives=[r for r in d.find(ly.music.items.Relative)]
print("Number of relatives: {}".format(len(relatives)))

for i in range(len(relatives)):
    print("Relative: {}".format(i))
    rel=relatives[i]
    c0 = [i for i in rel.find(ly.music.items.Command)][0]
    elements = [n for n in rel.find((ly.music.items.Note, ly.music.items.Rest, ly.music.items.PipeSymbol, ly.music.items.Command, ly.music.items.KeySignature))]

    notes=[]

    for elem in elements:
        if type(elem) == ly.music.items.Note:
            notes.append({'name': elem.pitch.output(), 'length': elem.length()})
        if type(elem) == ly.music.items.Rest:
            notes.append({'name': "Rest", 'length': elem.length()})

    for m in measures(notes):
        print("  |")
        for n in m:
            print("    "+n["name"])


# Test data
#notes=[]
#for i in range(100):
#    if i%2==0:
#        notes.append({'name': "B", 'length': fractions.Fraction(1, 8)})
#    else:
#        notes.append({'name': "A", 'length': fractions.Fraction(1, 8)})

def preprocessing(notes):
    namecat = sklearn.preprocessing.LabelEncoder().fit_transform([n["name"] for n in notes])
    onehotencoded = sklearn.preprocessing.OneHotEncoder().fit_transform([[n] for n in namecat]).todense()

    numerator = [n["length"].numerator for n in notes]
    denominator = [n["length"].denominator for n in notes]

    return numpy.append(numpy.append(onehotencoded, [[n] for n in numerator], axis=1), [[d] for d in denominator], axis=1)


data = preprocessing(notes).getA()
scaler = sklearn.preprocessing.MinMaxScaler()
scaled = scaler.fit_transform(data)
print(scaled.shape)

sequenceLength = 20
n_features = len(data[0])

input = numpy.zeros((len(scaled)-sequenceLength, sequenceLength, len(scaled[0])))
output = numpy.zeros((len(scaled)-sequenceLength, len(scaled[0])))
for i in range(0, len(scaled)-sequenceLength):
    for j in range(sequenceLength):
        input[i, j] = scaled[i+j]
    output[i] = scaled[i+sequenceLength]
print(input.shape)
print(output.shape)

model = Sequential()
model.add(LSTM(n_features, input_shape=(input.shape[1], input.shape[2]), return_sequences=True))
model.add(Dropout(0.1))
model.add(Dense(n_features))
#model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

fitted = model.fit(input, output, epochs=400, batch_size=20)

print(output[70])
print(scaler.inverse_transform([model.predict(input)[70]]))