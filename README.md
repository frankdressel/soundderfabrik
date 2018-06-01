# soundderfabrik

## Installation

```
  sudo add-apt-repository ppa:mscore-ubuntu/mscore-stable
  sudo apt-get update
  sudo apt-get install musescore
  
  pip install music21
  
  sudo apt-get install timidity
```

Taken from here: https://unix.stackexchange.com/a/97908

```
  sudo apt-get install fluid-soundfont-gm
  sudo sed -e 's|^source|#source|' -e '$a source /etc/timidity/fluidr3_gm.cfg' -i /etc/timidity/timidity.cfg
  sudo /etc/init.d/timidity restart
```
  
Inside python:

```
  from music21 import *
  environment.set('midiPath', '/usr/bin/timidity')
  environment.set('musicxmlPath', '/usr/bin/musescore')
```
