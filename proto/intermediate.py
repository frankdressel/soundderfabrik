# coding: utf-8
from music21 import *
import os
import requests
import tempfile

environment.set('autoDownload', 'allow')

exampleUrl="http://www.mutopiaproject.org/ftp/BachJS/BWV208/Sheep/Sheep.mid"

# First approach: Problems with non-existing triplets.
s=converter.parse(exampleUrl)
parts=[p.makeMeasures() for p in s.getElementsByClass(stream.Part)]
print("Anzahl der Stimmen", len(parts))

for n in list(parts[0].measures(0, 3).flat.getElementsByClass([note.Note, note.Rest])):
     if n.isNote:
         print(n, n.name, n.pitch.name, n.duration.fullName)
     if n.isRest:
         print("Rest", "-", n.duration.fullName)

# Second approach: No problems with triplets but totally wrong
r = requests.get(exampleUrl)
with tempfile.NamedTemporaryFile() as f:
    f.write(r.content)

    fp=f.name
    mf = midi.MidiFile()
    mf.open(str(fp))
    mf.read()
    mf.close()

    for i in range(len(mf.tracks)):
        print("Track {}".format(i))
        t=midi.translate.midiTrackToStream(mf.tracks[1], 96)
        for n in list(t.flat.getElementsByClass([note.Note, note.Rest])):
            if n.isNote:
                print(n.name, n.pitch.name, n.duration.fullName)
            if n.isRest:
                print("Rest", "-", n.duration.fullName)
            if n.isChord:
                print([n for n in element.normalOrder])

    f.close()

# Third approach: More complicated but correct
import ly.document
import ly.music
doc=ly.document.Document.load('/home/vagrant/Downloads/Sheep.ly')
d=ly.music.document(doc)

r0=[r for r in d.find(ly.music.items.Relative)][0]
c0=[i for i in r0.find(ly.music.items.Command)][0]
[n for n in r0.find((ly.music.items.Note, ly.music.items.Duration))][0:20]
