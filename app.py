import streamlit as st
import pickle
import pandas as pd
import requests



@st.cache_data(ttl=3600)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params={"api_key": st.secrets["TMDB_API_KEY"]},
                timeout=20
            )
            response.raise_for_status()

            data = response.json()
            poster_path = data.get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

            return None

        except requests.RequestException as e:
            if attempt == 2:
                print(f"Failed to fetch movie {movie_id}: {e}")
                return None

    return None



def recommend(movie):
   movie_index= movies[movies['title']==movie].index[0]
   distances= similarity[movie_index]
   movies_list= sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

   recommended_movies= []
   recommended_movies_posters=[]

   for i in movies_list: 
    movie_id= movies.iloc[i[0]].movie_id
    recommended_movies.append(movies.iloc[i[0]].title)
    # fetch poster
    recommended_movies_posters.append(fetch_poster(movie_id))
    
   return recommended_movies, recommended_movies_posters



st.title('Movie Recommender baby')
movies_dict= pickle.load(open('movies_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl','rb'))
selected_movie_name= st.selectbox(
    'Select a movie you like',
    movies['title'].values
)
if st.button('Recommend'):
    names, posters= recommend(selected_movie_name)
    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0]:
            st.image(posters[0])
        else:
            st.write("Poster unavailable")
    
    with col2:
       st.text(names[1])
       if posters[1]:
           st.image(posters[1])
       else:
           st.write("Poster unavailable")
    
    with col3:
       st.text(names[2])
       if posters[2]:
           st.image(posters[2])
       else:
           st.write("Poster unavailable")
    with col4:
       st.text(names[3])
       if posters[3]:
           st.image(posters[3])
       else:
           st.write("Poster unavailable")

    with col5:
       st.text(names[4])
       if posters[4]:
           st.image(posters[4])
       else:
           st.write("Poster unavailable")