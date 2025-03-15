import os
import regex as re
import subprocess
import urllib
import numpy as np
import time
from matplotlib import pyplot as plt
from music21 import converter, midi, stream
# from timidity import Parser, play_notes
from song_utils import play_notes
from midi_parser import Parser
from scipy.signal import square, sawtooth
from scipy.io import wavfile

from IPython.display import Audio
from IPython import display


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
def save_song_abc(song, filename=None):
    if filename is None:
        filename = "temp"
    save_path = os.path.join("data", filename + ".abc")
    with open(save_path, "w") as f:
        f.write(song)
    return filename


# Convert ABC notation to audio file
""" def abc2wav(abc, wav):
    cmd = f"abc2midi {abc} -o - | timidity -Ow -o {wav} -"
    return subprocess.call(cmd, shell=True) """


# Convert ABC to MIDI
def abc2midi(abc):
    # abc_file = f'{abc}.abc'
    conv = converter.parse(os.path.abspath(get_abc_path(abc)))
    output_path = os.path.abspath(get_midi_path(abc))
    midi = conv.write("midi", output_path)
    return midi


# ABC to WAV
def abc2wav(abc):
    wav_path = os.path.abspath(get_wav_path(abc))
    midi_path = abc2midi(abc)
    ps = Parser(midi_path)
    audio = play_notes(*ps.parse(), sawtooth, wait_done=False)
    wavfile.write(wav_path, 44100, audio)

# Play audio file


def play_wav(wav):
    print(f"Playing audio file: {wav}")
    return Audio(wav)


# Play the song
def play_song(song, filename=None):
    if filename is None:
        filename = "temp.wav"
    basename = save_song_abc(song, filename=filename)
    temp_abc = os.path.abspath(get_abc_path(basename))
    abc2wav(temp_abc)
    wav_path = os.path.abspath(get_wav_path(filename))
    if wav_path == 0:
        return "Error: Could not convert ABC to WAV"
    return play_wav(wav_path)

# Plotter


class Plotter:
    def __init__(self, sec, xlabel="", ylabel="", scale=None):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.sec = sec
        self.scale = scale

        self.tic = time.time()

    def plot(self, data):
        if time.time() - self.tic > self.sec:
            plt.cla()

            if self.scale is None:
                plt.plot(data)
            elif self.scale == "semilogx":
                plt.semilogx(data)
            elif self.scale == "semilogy":
                plt.semilogy(data)
            elif self.scale == "loglog":
                plt.loglog(data)
            else:
                raise ValueError(
                    "unrecognized parameter scale {}".format(self.scale))

            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            display.clear_output(wait=True)
            display.display(plt.gcf())

            self.tic = time.time()


# Getters
def get_midi_path(file):
    file = f'{file}.mid'
    return os.path.join("output", "midi", file)


def get_wav_path(file):
    file = f'{file}.wav'
    return os.path.join("output", "wav", file)


def get_abc_path(file):
    file = f'{file}.abc'
    return os.path.join("data", file)
