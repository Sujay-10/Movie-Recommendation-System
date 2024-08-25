import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    if movie_id is None:
        return "https://via.placeholder.com/500x750?text=Invalid+Movie+ID"

    api_key = '2c53f9ebf9245bec43da22dd0d7e7374'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.RequestException as e:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        if pd.isna(movie_id):
            continue
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('simirality.pkl', 'rb'))

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Search for the Movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
