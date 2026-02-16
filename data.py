import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import streamlit as st

load_dotenv()
st.set_page_config(
    page_title="Spotify Listening Intelligence",
    page_icon="🎵",
    layout="wide"
)


st.title("Spotify Listening Intelligence")

st.markdown("Welcome to Simran Chopra's Spotify Summary!!")
st.divider()

#st.subheader("Welcome to Simran Chopra's Spotify Summary!!")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-top-read"
))

# print(dir(sp))
# print(" ")
# help(sp.current_user_top_tracks)
# print(" ")

time_range = st.selectbox(
    "Select Time Range",
    ["Last Month", "Last 6 Months", "All Time"]
)

number_songs = st.slider(
    "Number of Songs",
    min_value=10,
    max_value=50,
    value=20
)

mapping = {
    "Last Month": "short_term",
    "Last 6 Months": "medium_term",
    "All Time": "long_term"
}
spotify_value = mapping[time_range]

results = sp.current_user_top_tracks(limit=number_songs, time_range=spotify_value)

tracks = []

for item in results["items"]:
    tracks.append({
        "name": item["name"],
        "artist": item["artists"][0]["name"],
        "duration_min": item["duration_ms"] / 60000,
        "explicit": item["explicit"]
    })

df = pd.DataFrame(tracks)


col1, col2, col3 = st.columns(3)

col1.metric("Avg Duration (min)", round(df["duration_min"].mean(), 2))
col2.metric("Unique Artists", df["artist"].nunique())

st.write("Top 10 songs:")
st.dataframe(df)
st.write("Average Duration:", round(df["duration_min"].mean(), 2))

artist_counts= df["artist"].value_counts()
print(artist_counts)

#matplotlib:
fig, ax = plt.subplots(figsize=(6, 2))

artist_counts.plot(kind="bar", ax=ax)
plt.title("Top Artists")
plt.ylabel("Number of Tracks")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
st.subheader("Artist Frequency Table")
st.dataframe(artist_counts)

st.divider()
st.caption("Built By Simran Chopra - Using Spotify API & Streamlit| Portfolio Project")
