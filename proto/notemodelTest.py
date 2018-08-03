import unittest
import notemodel

from keras import backend as K


class MyTestCase(unittest.TestCase):
    def testInit(self):
        """Test the setup of translation and reverse translation."""
        notes = ["a", "b", "c", "d", "e"]
        nm = notemodel.Model(notes)

        self.assertEqual(len(nm._vocab), 5)

        for n in notes:
            self.assertNotEqual(n, nm._translation[n])
            self.assertEqual(n, nm._reverse_translation[nm._translation[n]])

    def testInputOutput(self):
        notes = ["a", "b", "c", "d", "e"]
        num_timesteps = 3
        measure_length = 2

        nm = notemodel.Model(notes)

        inp, out = nm.create_input_output(notes, num_timesteps, measure_length)

        self.assertEqual(len(inp[0]), len(notes)-num_timesteps+1)
        for i in inp[0]:
            # The inut vector for each batch is the number of vocabulary entries plus one more entry for the position.
            self.assertEqual(len(i), len(nm._vocab)+1)

        # With a measure length of 2, there are just position 0/1.
        self.assertEqual(inp[0][0][-1], 0)
        self.assertEqual(inp[0][1][-1], 1)
        self.assertEqual(inp[0][2][-1], 0)

    def testLoss(self):
        notes = ["a", "cont", "c", "d", "e"]
        num_timesteps = 4
        measure_length = 2

        nm = notemodel.Model(notes)

        inp, out = nm.create_input_output(notes, num_timesteps, measure_length)

        inp_tensor = K.variable(K.cast_to_floatx(inp))
        out_tensor = K.variable(K.cast_to_floatx(out))

        loss_function = nm.loss(inp_tensor)
        score = K.eval(loss_function(out_tensor, out_tensor))

        # Same input should produce a score of 0.
        self.assertAlmostEqual(0, score[0], places=6)


if __name__ == '__main__':
    unittest.main()