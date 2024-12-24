import streamlit as st
import pickle
import pandas as pd

# Load the pickled data
with open('cosine_sim.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

with open('df.pkl', 'rb') as f:
    df = pickle.load(f)

# Ensure track names are lowercased for matching purposes
df['normalized_track_name'] = df['track_name'].str.strip().str.lower()

# Define the recommendation function
def get_recommendations(title, cosine_sim=cosine_sim):
    title = title.strip().lower()
    
    if title not in df['normalized_track_name'].values:
        return f"Song '{title}' not found in the dataset."
    
    idx = df[df['normalized_track_name'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    song_indices = [i[0] for i in sim_scores]
    
    recommendations = []
    for i in song_indices:
        track_name = df['track_name'].iloc[i]
        artist_name = df['artist_name'].iloc[i]
        recommendations.append(f"{track_name} by {artist_name}")
    
    return recommendations

# Streamlit app layout
st.title("Song Recommendation System")

# User input for song title
song_title = st.text_input("Enter a song title to get recommendations:")

# Show recommendations when user enters a song title
if song_title:
    recommendations = get_recommendations(song_title)
    
    # If recommendations are found, display them
    if isinstance(recommendations, str):  # Handle case where the song is not found
        st.error(recommendations)
    else:
        st.write(f"Here are the top recommendations for '{song_title}':")
        for song in recommendations:
            st.write(f"- {song}")
