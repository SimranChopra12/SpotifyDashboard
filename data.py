import os
import pandas as pd
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
if st.query_params.get("health") == "1":
    st.write("ok")
    st.stop()
st.set_page_config(
    page_title="Spotify Listening Intelligence",
    page_icon="🎵",
    layout="wide"
)

st.title("Spotify Listening Intelligence")

st.markdown("Welcome to Simran Chopra's Spotify Summary!!")
st.write("Here’s how I analyze user behavior, identify product risks, and design experiments to improve engagement")
st.divider()

df = pd.read_csv("spotify_dataset.csv")

time_range = st.selectbox(
    "Select Time Range",
    ["Last Month", "Last 6 Months", "All Time"]
)
user_type = st.selectbox(
    "User Segment",
    ["Balanced", "Loyalist (High Concentration)", "Explorer (High Diversity)"]
)
number_songs = st.slider(
    "Number of Songs",
    min_value=10,
    max_value=50,
    value=20
)

if user_type == "Balanced":
    df = pd.read_csv("spotify_dataset.csv")
elif user_type == "Loyalist (High Concentration)":
    df = pd.read_csv("loyalist.csv")
else:
    df = pd.read_csv("explorer.csv")

col1, col2, col3 = st.columns(3)

col1.metric("Avg Duration (min)", round(df["duration_min"].mean(), 2))
col2.metric("Unique Artists", df["artist"].nunique())

st.write("Top 10 songs:")
st.dataframe(df)
st.write("Average Duration:", round(df["duration_min"].mean(), 2))

artist_counts= df["artist"].value_counts()
print(artist_counts)
most_common_artist = artist_counts.idxmax()

st.markdown(f"""
### Listening Insight
You are currently most focused on **{most_common_artist}**.
""")

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

shares = df["artist"].value_counts(normalize=True)
hhi = float((shares ** 2).sum())

st.metric("Listening Concentration (HHI)", round(hhi, 3))


st.divider()
st.caption("Built By Simran Chopra - Using Spotify API & Streamlit| Portfolio Project")