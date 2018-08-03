import keras
import numpy

from keras import backend as K

class Model():

    def __init__(self, notes):
        """
        :param notes: A list of string symbols indicating the notes.
        """
        self._notes=notes
        self._vocab = numpy.unique(notes)
        self._categories = range(0, len(self._vocab))
        self._translation = dict(zip(self._vocab, self._categories))
        self._reverse_translation = dict(zip(self._categories, self._vocab))

        self._num_features=len(self._vocab)

    def loss(self, input_tensor):
        def cat(y_true, y_pred):
            # The position for each batch of the note BEFORE the prediction note.
            pos=K.flatten(input_tensor[:,-1,-1])
            first_position=(pos==0)

            zeros=K.zeros_like(y_pred)
            translated = self._translation["cont"]
            onehot = numpy.zeros(self._num_features)
            onehot[translated] = 1
            score=0
            if not K.is_placeholder(y_true):
                onehot_matrix=K.variable(K.cast_to_floatx(numpy.tile(onehot, [K.int_shape(y_true)[0], 1])))
                score=50#K.batch_dot(y_pred, onehot_matrix, axes=1)

            return keras.losses.categorical_crossentropy(y_true, y_pred)#+10*score#*K.sum(K.cast(first_position, "float32")*K.cast(cont, "float32"))

        return cat

    def create_input_output(self, notes, num_timesteps, measure_length):
        input_x = []
        input_y = []
        for i in range(0, len(self._notes) - num_timesteps):
            part = notes[i:i + num_timesteps]
            translated = [self._translation[p] for p in part]
            onehot = numpy.zeros((len(part), self._num_features + 1))
            onehot[numpy.arange(len(part)), translated] = 1
            for j in range(num_timesteps):
                onehot[j][self._num_features] = (i + j) % measure_length
            input_x.append(onehot)

            translated = [self._translation[p] for p in notes[i + num_timesteps:i + num_timesteps + 1]]
            onehot = numpy.zeros(self._num_features)
            onehot[translated] = 1
            input_y.append(onehot)

        input_x = numpy.array(input_x)
        input_y = numpy.array(input_y)

        return (input_x, input_y)