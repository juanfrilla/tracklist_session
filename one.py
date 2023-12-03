# TODO meterle una sesión y que me devuelva el tracklist con la librería de shazam
# TODO hacerlo asincrono
# TODO meterle variables

from pydub import AudioSegment
import os, asyncio
from shazamio import Shazam


def list_to_txt(my_list):
    with open("tracklist.txt", mode="w") as file:
        for item in my_list:
            file.write("%s\n" % item)


async def identify_song(path):
    print("identificando canción")
    shazam = Shazam()
    out = await shazam.recognize_song(f"{path}")
    if os.path.exists(path):
        os.remove(path)
    return out


async def split_session_recognize(audio_input):
    # Load the MP3 file
    audio = AudioSegment.from_file(audio_input, format="mp3")

    # Get the length of the audio in milliseconds
    audio_length = len(audio)

    # Set the duration of each segment in milliseconds
    segment_duration = 60 * 1000  # 1 minute

    song_list = []

    for start_time in range(0, audio_length, segment_duration):
        end_time = start_time + segment_duration
        if end_time > audio_length:
            end_time = audio_length
        segment = audio[start_time:end_time]
        output_file = f"segment.mp3"
        segment.export(output_file, format="mp3")

        song_dict = {"title": "", "artists": ""}
        song = await identify_song("segment.mp3")

        song_dict["title"] = song.get("track", {}).get("title", "")
        song_dict["artists"] = song.get("track", {}).get("subtitle", "")

        if song_dict in song_list and song_dict != {"title": "", "artists": ""}:
            continue
        song_list.append(song_dict)
    return song_list



if __name__ == "__main__":
    import time
    start = time.time()
    file = "session.mp3"
    song_dict = asyncio.run(split_session_recognize(file))
    list_to_txt(song_dict)
    end = time.time()
    timix = end - start
    print("Tiempo", timix)