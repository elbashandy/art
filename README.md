# art
My sandbox of artistic creations

## Easy/Clean Programming Environment on your Computer

For a clean environment, and for easier runs, use either [`conda`](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or [`virtualenv`](https://virtualenv.pypa.io/en/latest/user_guide.html) to install the libraries.

## Projects
### Audio Visualization

A python script draws circles in random spots to correspond to a given audio input for visualization.

This script was tested with Python 3.6.

To install the necessary libraries:
```sh
pip3 install -r audio_visuals/requirements.txt
```

To run the script on an audio file of your choice:
```sh
audio_visuals/play.py --audio [audiofile]
```

There are two sample audio files on which the script could be tested:

```
# relaxing music
python audio_visuals/play.py --audio audio/rudra_mantra.wav

# intense music
python audio_visuals/play.py --audio audio/ekhwati.wav
```

### Agency Fusion in Media

A python script that simulates a network that is structered on a random basis and other factors. The simulation is a basic abstracted template of the relationships that formulate between actants. It touches the fields of Affect theory and Actor-Network theory.

The script was run through Python 3.9.

To install the necessary libraries:
```sh
pip3 install -r agency_fusion/requirements.txt
```

To run the script:
```sh
agency_fusion/life.py
```

