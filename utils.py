import os
import regex as re
import subprocess
import urllib
import numpy as np
from music21 import converter, midi, stream
from timidity import Parser, play_notes
from scipy.signal import square, sawtooth
from scipy.io import wavfile

from IPython.display import Audio


def test():
    print("Hello World")


# Load the data
def load_data():
    with open(os.path.join('data', 'sngs.abc'), 'r') as f:
        text = f.read()
    songs = extract_song_snippet(text)
    return songs


# Extract songs from the text
def extract_song_snippet(text):
    pattern = "(^|\n\n)(.*?)\n\n"
    search_results = re.findall(
        pattern, text, overlapped=True, flags=re.DOTALL)
    songs = [song[1] for song in search_results]
    print("Found {} songs in text".format(len(songs)))
    return songs


# Save song to ABC format
def save_song_abc(song, filename="temp"):
    save_path = "/data/{}.abc".format(filename)
    with open(save_path, "w") as f:
        f.write(song)
    return filename


# Convert ABC notation to audio file
def abc2wav(abc, wav):
    cmd = f"abc2midi {abc} -o - | timidity -Ow -o {wav} -"
    return subprocess.call(cmd, shell=True)


# Convert ABC to MIDI
def abc2midi(abc):
    conv = converter.parse(abc)
    output_path = os.path.join("output", "midi")
    conv.write("midi", os.path.join(output_path, "temp.mid"))


# Play audio file
def play_wav(wav):
    return Audio(wav)


# Play the song
