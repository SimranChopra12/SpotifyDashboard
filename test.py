# this just checks connection and prints top 5 songs

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
# loads env variables from .env

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read user-read-recently-played"
))
# setting up authentication - to access data - you cant just access it with API keys

results = sp.current_user_top_tracks(limit=15)

for i, item in enumerate(results["items"], start=1):
    print(f"{i}. {item['name']} - {item['artists'][0]['name']}")

