# coding: utf-8
import collections
import os
import requests
import tempfile

import ly.document
import ly.music
doc=ly.document.Document.load('/home/vagrant/Downloads/Sheep.ly')
d=ly.music.document(doc)

r0=[r for r in d.find(ly.music.items.Relative)][0]
c0=[i for i in r0.find(ly.music.items.Command)][0]
elements=[n for n in r0.find((ly.music.items.Note, ly.music.items.Duration, ly.music.items.PipeSymbol, ly.music.items.Command, ly.music.items.KeySignature))][0:20]

note=[]

for elem in elements:
    if type(elem)==ly.music.items.Note:
        note.append({'name': elem.pitch.output(), 'length': '{}/{}'.format(elem.length().numerator, elem.length().denominator)})
print(note)
