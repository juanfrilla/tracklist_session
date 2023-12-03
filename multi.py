from pydub import AudioSegment
import os, asyncio
from shazamio import Shazam
import concurrent.futures

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


def identify_multiple_songs(path):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(identify_song(path))

async def split_session_recognize(audio_input):
    # Load the MP3 file
    audio = AudioSegment.from_file(audio_input, format="mp3")

    # Get the length of the audio in milliseconds
    audio_length = len(audio)

    # Set the duration of each segment in milliseconds
    segment_duration = 60 * 1000  # 1 minute

    song_list = []
    for start_time in range(0, audio_length, segment_duration*4):
        four_song_list = []
        for i in range(4):
            end_time = start_time + segment_duration
            if end_time > len(audio):
                end_time = len(audio)
            segment = audio[start_time:end_time]
            output_file = f"segment_{i}.mp3"
            segment.export(output_file, format="mp3")
            four_song_list.append(output_file)
            start_time += segment_duration

        
        with concurrent.futures.ProcessPoolExecutor() as pool:
            futures = [
                loop.run_in_executor(pool, identify_multiple_songs, element)
                for element in four_song_list
            ]
        
        try:
            identified_songs = await asyncio.gather(*futures)
        except Exception as e:
            continue

        song_dict = {"title": "", "artists": ""}
        for song in identified_songs:
            song_dict["title"] = song.get("track", {}).get("title", "")
            song_dict["artists"] = song.get("track", {}).get("subtitle", "")

            if song_dict in song_list and song_dict != {"title": "", "artists": ""}:
                continue
            song_list.append(song_dict)
    return song_list

if __name__ == "__main__":
    import time
    start = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    song_list = loop.run_until_complete(split_session_recognize("session.mp3"))
    list_to_txt(song_list)
    end = time.time()

    timix = end - start
    print("Tiempo", timix)