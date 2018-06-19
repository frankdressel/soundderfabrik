# coding: utf-8
from music21 import *
import os
import tempfile

environment.set('autoDownload', 'allow')

exampleUrl="http://www.mutopiaproject.org/ftp/BachJS/BWV208/Sheep/Sheep.mid"

# First approach: Problems with non-existing triplets.
s=converter.parse(exampleUrl)
parts=[p.makeMeasures() for p in s.getElementsByClass(stream.Part)]
print("Anzahl der Stimmen", len(parts))

for n in list(parts[0].measures(3, 3).flat.getElementsByClass([note.Note, note.Rest])):
     if n.isNote:
         print(n.name, n.pitch.name, n.duration.fullName)
     if n.isRest:
         print("Rest", "-", n.duration.fullName)

# Second approach: No problems with triplets.
fp=os.path('home/vagrant/Download/Sheep.mid')
mf = midi.MidiFile()
mf.open(str(fp))
mf.read()
mf.close()

for i in range(len(mf.tracks)):
    print("Track {}".format(i))
    t=midi.translate.midiTrackToStream(mf.tracks[1], 96*2).makeMeasures()
    for n in list(t.measures(3, 3).flat.getElementsByClass([note.Note, note.Rest])):
        if n.isNote:
            print(n.name, n.pitch.name, n.duration.fullName)
        if n.isRest:
            print("Rest", "-", n.duration.fullName)
