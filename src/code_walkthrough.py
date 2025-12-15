import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
from pathlib import Path

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


print(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI)


playlist_url = "https://open.spotify.com/playlist/2km2nHDVADmnQMhQRaTOEL"

playlist_id=playlist_url.split("playlist/")[1].split("?")[0]

print(playlist_id)