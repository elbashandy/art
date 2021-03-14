# art
My sandbox of artistic creations

## Projects
### Audio Visualization

A python script draws circles in random spots to correspond to a given audio input for visualization.

This script was tested with Python 3.6.

For a clean environment, use either [`conda`](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or [`virtualenv`](https://virtualenv.pypa.io/en/latest/user_guide.html) to install the libraries.

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
