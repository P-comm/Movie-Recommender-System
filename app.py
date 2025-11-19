import streamlit as st
import pickle

import requests
import time


def fetch_poster(movie_id):
    api_key = "00b71ca5923bb588d147dd7f83949ac8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    for attempt in range(2):   # Retry 2 times
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "poster_path" in data and data["poster_path"]:
                return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"

        except Exception:
            time.sleep(0.3)  # wait and retry

    return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movie_list:
        idx = i[0]
        movie_id = movies.iloc[idx].movie_id

        # avoid too many API calls
        time.sleep(0.25)

        recommended_movie_names.append(movies.iloc[idx].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
