import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


print(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI)


def extract_playlist_id(link):
    return link.split("playlist/")[1].split("?")[0]

def fetch_playlist(playlist_link):
    playlist_id = extract_playlist_id(playlist_link)

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="playlist-read-private playlist-read-collaborative"
        )
    )


    results = sp.playlist_items(playlist_id, additional_types=["track"])
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    for i, item in enumerate(tracks):
        track = item["track"]
        if not track:
            continue
        print(f"{i+1}. {track['name']} — {', '.join([a['name'] for a in track['artists']])}")
        print(f"    Album: {track['album']['name']}")
        print(f"    Track ID: {track['id']}")
        print(f"    Duration (ms): {track['duration_ms']}")
        print("-" * 40)

if __name__ == "__main__":
    playlist_url = "https://open.spotify.com/playlist/2km2nHDVADmnQMhQRaTOEL?si=fMi8UPf6QLqvhsTn_2mdwA"
    fetch_playlist(playlist_url)
