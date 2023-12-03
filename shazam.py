import os

from shazamio import Shazam

class ShazamHelper():
    async def identify_song(self, path):
        print("identificando canción")
        shazam = Shazam()
        out = await shazam.recognize_song(f"{path}")
        if os.path.exists(path):
            os.remove(path)

        if "track" in out:
            providers = out["track"]["hub"]["providers"]

            for provider in providers:
                if (
                    provider["type"] == "SPOTIFY"
                    and "spotify:search:" in provider["actions"][0]["uri"]
                ):
                    return provider["actions"][0]["uri"]
        else:
            return None