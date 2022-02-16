
import streamlit as st
import pickle
import pandas as pd
import requests
import base64


main_bg = "mov2.jpg"
main_bg_ext = "jpg"

side_bg = "mov2.jpg"
side_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
   .sidebar .sidebar-content {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)





def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_posters = []
    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,recommended_movie_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('',movies['title'].values)



if st.button('Recommend movies'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:

        st.image(recommended_movie_posters[0])
        st.text(recommended_movie_names[0])


    with col2:

        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_names[1])

    with col3:

        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_names[2])

    with col4:

        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_names[3])

    with col5:

        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_names[4])



