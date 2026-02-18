import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


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
st.subheader("Top Artists")

fig = px.bar(
    artist_counts,
    x=artist_counts.index,
    y=artist_counts.values,
    labels={"x": "Artist", "y": "Number of Tracks"},
    title="Top Artists"
)

fig.update_traces(marker_color="black")
fig.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

# st.subheader("Artist Frequency Table")
# st.dataframe(artist_counts)

st.divider()
st.caption("Built By Simran Chopra - Using Spotify API & Streamlit| Portfolio Project")



all_genres =[]



