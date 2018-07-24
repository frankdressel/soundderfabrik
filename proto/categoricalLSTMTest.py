import numpy
import unittest
import categoricalLSTM

class MyTestCase(unittest.TestCase):
    def testSimpleCategoricalLSTM_I(self):
        leval=categoricalLSTM.SimpleCategoricalLSTM()

        num_batches = 100

        input_x=numpy.tile([[1, 2, 3], [2, 3, 4]], (num_batches, 1, 1))
        input_y=numpy.tile([1, 0, 0], (num_batches, 1))

        result=leval.fit((input_x, input_y))

        # Hot encoding and softmax: Should be close with 1% deviation.
        self.assertTrue(numpy.allclose(input_y, result, atol=1e-02))

if __name__ == '__main__':
    unittest.main()
