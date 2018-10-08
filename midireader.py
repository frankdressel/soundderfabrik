import unittest
from collections import Counter
from dataclasses import dataclass
import numpy
import random

import mido


class StreamProcessor:
    """
    Class for reading and analysing streams (lists) of mido messages.
    """

    def stream_to_notes(self, stream):
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
            offset = 0
            for index, msg in enumerate([s for s in stream if not s.is_meta]):
                if msg.time is not None:
                    time = time + msg.time
                if msg.channel == channel:
                    if msg.note in current_notes:
                        start_time = current_notes[msg.note]
                        notes_at_starttime = notes.get(start_time, [])
                        notes_at_starttime.append(Note(msg.note, time - start_time, offset))
                        offset = 0
                        notes[start_time] = notes_at_starttime
                        del current_notes[msg.note]
                    else:
                        current_notes[msg.note] = time
                        offset = offset + msg.time
                else:
                    offset = offset + msg.time

            _result = []
            for (key, _) in sorted(notes.items()):
                if len(notes[key]) > 1:
                    _result.append(Accord(tuple(notes[key])))
                else:
                    _result.append(notes[key][0])

            result.append(_result)
        return result

    def notes_to_stream(self, notes):
        result = []
        for i in range(len(notes)):
            result.append(mido.Message('note_on', note=notes[i].name, velocity=90,
                                       time=notes[i].offset))
            result.append(mido.Message('note_on', note=notes[i].name, velocity=0,
                                       time=notes[i].duration))

        return result

class Analyser:
    """
    Class for analysing streams of Notes.
    """
    length = 4

    def analyse(self, stream):
        """
        Analyse a stream of Notes with regard to NGrams.
        """
        ngrams = []
        for i in range(len(stream)):
            for j in range(min(len(stream), self.length, i+1)):
                ngrams.append(NGram(tuple(stream[i - j:i+1])))

        return ngrams

@dataclass(frozen=True)
class Note:
    """
    Represents a note.
    """
    name: ""
    duration: 0
    offset: 0

@dataclass(frozen=True)
class Accord:
    """
    Represents an accord as a tuple of Notes.
    """
    notes: tuple

@dataclass(frozen=True)
class NGram:
    notes: tuple

    def reduce(self):
        return NGram(self.notes[:-1]), self.notes[-1]

class StreamProcessorTest(unittest.TestCase):
    def test_stream_to_notes(self):
        notemessages = [
            mido.Message('note_on', note=70, time=1, channel=0, velocity=90),
            mido.Message('note_on', note=70, time=1, channel=0, velocity=0),
            mido.Message('note_on', note=75, time=0, channel=0, velocity=90),
            mido.Message('note_on', note=70, time=0, channel=1, velocity=90),
            mido.Message('note_on', note=75, time=1, channel=0, velocity=0),
            mido.Message('note_on', note=70, time=1, channel=1, velocity=0),
            mido.Message('note_on', note=90, time=1, channel=0, velocity=90),
            mido.Message('note_on', note=90, time=1, channel=0, velocity=0),
        ]
        result = StreamProcessor().stream_to_notes(notemessages)[0]

        self.assertEqual(result[0], Note(70, 1, 1))
        self.assertEqual(result[1], Note(75, 1, 0))
        self.assertEqual(result[2], Note(90, 1, 2))

    def test_notes_to_stream(self):
        notemessages = [
            mido.Message('note_on', note=70, time=1, channel=0, velocity=90),
            mido.Message('note_on', note=70, time=1, channel=0, velocity=0),
            mido.Message('note_on', note=75, time=0, channel=0, velocity=90),
            mido.Message('note_on', note=70, time=0, channel=1, velocity=90),
            mido.Message('note_on', note=75, time=1, channel=0, velocity=0),
            mido.Message('note_on', note=70, time=1, channel=1, velocity=0),
            mido.Message('note_on', note=90, time=1, channel=0, velocity=90),
            mido.Message('note_on', note=90, time=1, channel=0, velocity=0),
        ]
        notes = StreamProcessor().stream_to_notes(notemessages)[0]
        result = StreamProcessor().notes_to_stream(notes)

        self.assertEqual(result[0], mido.Message('note_on', note=70, time=1, channel=0, velocity=90))
        self.assertEqual(result[1], mido.Message('note_on', note=70, time=1, channel=0, velocity=0))
        self.assertEqual(result[2], mido.Message('note_on', note=75, time=0, channel=0, velocity=90))
        self.assertEqual(result[3], mido.Message('note_on', note=75, time=1, channel=0, velocity=0))
        # We are just looking at channel 0 events and thus the channel 1 event
        # increases the time from 1 to 2.
        self.assertEqual(result[4], mido.Message('note_on', note=90, time=2, channel=0, velocity=90))
        self.assertEqual(result[5], mido.Message('note_on', note=90, time=1, channel=0, velocity=0))
        

    def test_song2(self):
        mid = mido.midifiles.MidiFile("/home/frank/Downloads/alkan-op31-8.mid")
        StreamProcessor().stream_to_notes([m for m in mid])[0]

        mid_out = mido.MidiFile()
        track = mido.MidiTrack()
        mid_out.tracks.append(track)

        for msg in [m for m in mid if m.is_meta or m.channel == 0]:
            if not msg.is_meta:
                msg.time = int(mido.second2tick(msg.time, 8, 10000))
            track.append(msg)

        mid_out.save('new_song.mid')

class NGramTest(unittest.TestCase):
    """
    Test case for NGrams
    """
    def test_creation(self):
        """
        Tests the creation of NGrams.
        """
        NGram((Note("a", 1, 0), Note("b", 2, 0)))

    def test_dict(self):
        """
        Tests, if the instances of an NGram with the same notes are equal in a
        dictionary.
        """
        ngram_dict = dict()
        ngram_one = NGram((Note("a", 1, 0), Note("b", 2, 0)))
        ngram_two = NGram((Note("a", 1, 0), Note("b", 2, 0)))
        ngram_dict[ngram_one] = 1
        self.assertTrue(ngram_two in ngram_dict)

    def test_reduce(self):
        ngram = NGram((Note("a", 1, 0), Note("b", 2, 0)))
        self.assertEqual(ngram.reduce()[0], NGram((Note("a", 1, 0), )))
        self.assertEqual(ngram.reduce()[1], Note("b", 2, 0))

class AnalyserTest(unittest.TestCase):
    def test_analyse(self):
        analyser = Analyser()
        result1 = analyser.analyse([Note("a", 1, 0)])
        self.assertEqual(1, len(result1))

        result2 = analyser.analyse([Note("a", 1, 0), Note("b", 2, 0)])
        self.assertEqual(3, len(result2))

        result3 = analyser.analyse([Note("a", 1, 0), Note("b", 2, 0), Note("c", 1, 0), Note("d", 2, 0), Note("e", 1, 0), Note("b", 2, 0)])
        self.assertEqual(18, len(result3))

        result4 = analyser.analyse([Note("a", 1, 0), Note("b", 2, 0), Note("a", 1, 0), Note("b", 2, 0), Note("a", 1, 0), Note("b", 2, 0)])
        self.assertEqual(18, len(result4))

if __name__ == '__main__':

    mid = mido.midifiles.MidiFile("/home/frank/Downloads/alkan-op31-8.mid")
    notes = StreamProcessor().stream_to_notes([m for m in mid.tracks[1]])[0]

    analyser = Analyser()
    ngrams = analyser.analyse(notes)

    reduced_ngrams={}
    for ngram in ngrams:
        reduced, following = ngram.reduce()
        l = reduced_ngrams.get(reduced, [])
        l.append(following)
        reduced_ngrams[reduced] = l

    for i in range(500):
        lasttwo = NGram(tuple(notes[-2:]))
        if lasttwo in reduced_ngrams:
            c = Counter(reduced_ngrams[lasttwo])
            total = sum(c.values())
            rand = random.randint(0, total)
            summed = 0
            for k in c.keys():
                summed = summed + c[k]
                if summed >= rand:
                    notes.append(k)
                    break
        else:
            c = Counter(notes)
            total = sum(c.values())
            rand = random.randint(0, total)
            summed = 0
            for k in c.keys():
                summed = summed + c[k]
                if summed >= rand:
                    notes.append(k)
                    break

    mid_out = mido.MidiFile(type=1, ticks_per_beat = mid.ticks_per_beat)
    mid_out.tracks.append(mid.tracks[0])
    track = mido.MidiTrack()
    mid_out.tracks.append(track)

    messages = StreamProcessor().notes_to_stream(notes)
    for msg in messages:
        track.append(msg)

    mid_out.save('new_song.mid')

    find_me = NGram(tuple(notes[-1:]))
    #print(reduced_ngrams)
    #print(reduced_ngrams[find_me])
