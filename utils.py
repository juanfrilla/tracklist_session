import re, time
from difflib import SequenceMatcher

from pydub import AudioSegment

# rom parallel.threadingresult import ThreadWithReturnValue


def get_1_minute_song(path):
    sound = AudioSegment.from_file(path)

    halfway_point = len(sound) // 2
    first_half = sound[halfway_point:]

    # create a new file "first_half.mp3":
    first_half.export(path, format="mp3")