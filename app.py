import json
import requests # type: ignore
import streamlit as st # type: ignore
import pickle
import pandas as pd # type: ignore

st.set_page_config(
        page_title="Movie Recommender System",
        page_icon="🎬",
        layout="wide",
        #initial_sidebar_state="expanded"
    )

def fetch_poster(movie_id):
    # Construct the API URL
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3e0cd48c96bc5c7ff61c95ed984853f2&language=en-US"
    
    try:
        
        response = requests.get(url)
        
        data = response.json()
        
        # Print the full response for debugging
        #print("API Response:")
        #print(json.dumps(data, indent=4))  # Pretty-print the JSON response
        
        # Check if 'poster_path' exists in the response
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            #print("Poster path not found in the response!")
            return "https://via.placeholder.com/500"  # Default placeholder image
    except Exception as e:
        # Print error details for debugging
        #print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500"  # Return placeholder on error
    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True , key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    names , posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4 , col5  = st.columns(5)
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