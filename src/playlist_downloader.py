import os
import csv
from pathlib import Path

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Load .env for local development (safe in GitHub Actions – it just does nothing)
load_dotenv()

# ---- Load credentials (support both naming conventions) ----
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET")

# ---- Fail fast if credentials are missing ----
if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        "Spotify credentials not found.\n"
        "Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET as environment variables."
    )


def extract_playlist_id(playlist_url: str) -> str:
    """Extract playlist ID from Spotify playlist URL."""
    return playlist_url.split("playlist/")[1].split("?")[0]


def fetch_playlist_to_csv(playlist_url: str, output_csv: str) -> None:
    playlist_id = extract_playlist_id(playlist_url)

    # Resolve project root → data folder
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / output_csv

    # ---- Spotify client (Client Credentials flow) ----
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
    )

    # ---- Fetch playlist items (pagination-safe) ----
    results = sp.playlist_items(playlist_id, additional_types=["track"])
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    # ---- Write results to CSV ----
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
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
            track = item.get("track")
            if not track:
                continue

            writer.writerow({
                "track_name": track["name"],
                "artists": ", ".join(artist["name"] for artist in track["artists"]),
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
