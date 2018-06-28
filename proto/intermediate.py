# coding: utf-8
import collections
import fractions
import os
import requests
import tempfile

import ly.document
import ly.music
doc=ly.document.Document.load('/home/vagrant/Downloads/Sheep.ly')
d=ly.music.document(doc)

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
    c0=[i for i in rel.find(ly.music.items.Command)][0]
    elements=[n for n in rel.find((ly.music.items.Note, ly.music.items.Rest, ly.music.items.PipeSymbol, ly.music.items.Command, ly.music.items.KeySignature))]

    notes=[]

    for elem in elements:
        if type(elem)==ly.music.items.Note:
            notes.append({'name': elem.pitch.output(), 'length': elem.length()})
        if type(elem)==ly.music.items.Rest:
            notes.append({'name': "Rest", 'length': elem.length()})

    for m in measures(notes):
        print("  |")
        for n in m:
            print("    "+n["name"])

relatives[1].dump()
