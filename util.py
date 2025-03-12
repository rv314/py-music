import os
import regex as re
import subprocess
import urllib
import numpy as np

from IPython.display import Audio

def load_data():
  with open(os.path.join('data', 'sngs.abc'), 'r') as f:
    text = f.read()
  songs = extract_song_snippet(text)
  return songs

def extract_song_snippet(text):
  pattern = "(^|\n\n)(.*?)\n\n"
  search_results = re.findall(pattern, text, overlapped=True, flags=re.DOTALL)
  songs = [song[1] for song in search_results]
  print("Found {} songs in text".format(len(songs)))
  return songs