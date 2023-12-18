import os
from shazamio import Shazam
import asyncio


def process_audio_async(audio_content):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(split_session_recognize(audio_content))


async def identify_song(path):
    print("identificando canción")
    shazam = Shazam()
    out = await shazam.recognize_song(f"{path}")
    if os.path.exists(path):
        os.remove(path)
    return out


async def split_session_recognize(audio):
    audio_length = len(audio)

    segment_duration = 60 * 1000

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
