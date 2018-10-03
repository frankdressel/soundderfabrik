import unittest
import numpy

import mido


class StreamReader:

    def event(self, stream):
        """
        Parameters
        ----------
        stream: list
            List of mido.Message objects

        Returns
        -------
        A list of lists of Note objects. The first dimension denotes the 
        channel and the second the note index within each channel.
        """
        result = []

        channels = numpy.unique([m.channel for m in stream if type(m) == mido.Message])
        for channel in channels:
            time = 0
            current_notes = {}
            notes = {}
            for msg in [s for s in stream if type(s) == mido.Message and s.channel == channel]:
                if msg.time is not None:
                    time = time + msg.time
                if msg.note is not None:
                    if msg.note in current_notes:
                        start_time = current_notes[msg.note]
                        notes_at_starttime = notes.get(start_time, [])
                        notes_at_starttime.append(Note(msg.note, time - start_time))
                        notes[start_time] = notes_at_starttime
                        del current_notes[msg.note]
                    else:
                        current_notes[msg.note] = time
            _result = []
            for (key, value) in sorted(notes.items()):
                if len(notes[key]) > 1:
                    _result.append(Accord(notes[key]))
                else:
                    _result.append(notes[key][0])

            result.append(_result)
        return result


class BaseSymbol:
    name: ""
    duration: 0

class Note(BaseSymbol):

    def __init__(self, name, duration):
        super().__init__()
        self.name = name
        self.duration = duration

    def __eq__(self, other):
        if self.name == other.name and self.duration == other.duration:
            return True
        return False

    def __repr__(self):
        return "{}-{};".format(self.name, self.duration)

class Accord(BaseSymbol):

    def __init__(self, notes):
        super().__init__()


class StreamReaderTest(unittest.TestCase):
    def test_event(self):
        on_message = mido.Message('note_on', note=60)
        off_message_1 = mido.Message('note_off', note=60, time=1)
        off_message_2 = mido.Message('note_on', note=60, velocity=0, time=1)
        result_1 = StreamReader().event([on_message, off_message_1])
        result_2 = StreamReader().event([on_message, off_message_2])
        self.assertEqual(1, len(result_1))
        self.assertEqual(1, len(result_2))
        self.assertEqual(Note(60, 1), result_1[0][0])
        self.assertEqual(Note(60, 1), result_2[0][0])

    def test_song(self):
        mid = mido.midifiles.MidiFile("Downloads/alkan-op31-8.mid")
        print(StreamReader().event([m for m in mid])[0])

        mid_out = mido.MidiFile()
        track = mido.MidiTrack()
        mid_out.tracks.append(track)

        for msg in [m for m in mid if m.is_meta or m.channel == 0]:
            if not msg.is_meta:
                msg.time = int(mido.second2tick(msg.time, 8, 10000))
            print(msg)
            track.append(msg)

        mid_out.save('new_song.mid')


if __name__ == '__main__':
    unittest.main()
