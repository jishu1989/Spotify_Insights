import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
from pathlib import Path

load_dotenv()

output_path = r"C:/Users/Soumya Das/Documents/git_projects/Spotify_Insightsspotify_playlist_data.csv"


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


print(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI)


def extract_playlist_id(link):
    return link.split("playlist/")[1].split("?")[0]

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
from pathlib import Path

load_dotenv()

#output_path = r"C:/Users/Soumya Das/Documents/git_projects/Spotify_Insightsspotify_playlist_data.csv"


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


print(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI)


def extract_playlist_id(link):
    return link.split("playlist/")[1].split("?")[0]

def fetch_playlist_to_csv(playlist_input, output_csv):
    playlist_id = extract_playlist_id(playlist_input)

    # Resolve repo root → data folder
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / output_csv

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

    # Open CSV file
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "track_name",
                "artists",
                "album",
                "release_date",
                "duration_ms",
                "popularity",
                "track_id"
            ]
        )
        writer.writeheader()

        for item in tracks:
            track = item["track"]
            if not track:
                continue

            writer.writerow({
                "track_name": track["name"],
                "artists": ", ".join(a["name"] for a in track["artists"]),
                "album": track["album"]["name"],
                "release_date": track["album"]["release_date"],
                "duration_ms": track["duration_ms"],
                "popularity": track["popularity"],
                "track_id": track["id"]
            })

    print(f"CSV saved at: {output_path}")


if __name__ == "__main__":
    playlist_url = "https://open.spotify.com/playlist/2km2nHDVADmnQMhQRaTOEL"
    fetch_playlist_to_csv(playlist_url, "spotify_playlist_data.csv")
