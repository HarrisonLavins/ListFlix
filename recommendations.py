import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Get information about a movie from dataset to be used for further preprocessing
def get_data():
    movie_data = pd.read_csv('dataset/movie_data.csv')
    # movie_data['original_title'] = movie_data['original_title'].str.lower()
    movie_data['movie_id'] = movie_data['movie_id']
    # print('---------- Movie Data -----------')
    # print(movie_data)
    return movie_data


# Drop the columns not used for feature extraction and combine cast and genres; return the combined column

def combine_data(data):
    data_recommend = data.drop(columns=['movie_id', 'original_title', 'plot'])
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(
        lambda x: ','.join(x.dropna().astype(str)), axis=1)
    data_recommend = data_recommend.drop(columns=['cast', 'genres'])
    return data_recommend


# Take the value returned by combine_data() and the plot column from get_data() and
# apply CountVectorizer and TfidfVectorizer respectively and calculates the Cosine values.
def transform_data(data_combine, data_plot):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data_combine['combine'])

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data_plot['plot'])

    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')

    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)

    return cosine_sim


# Recommend movies. The function recommend_movies() takes four parameters:
# title (name of the movie), data (return value of get_data()), combine (return value of combine_data()) and,
# transform (return value of transform_data()). It returns a Pandas DataFrame with the top 20 movie recommendations
def recommend_movies(movie_id, data, combine, transform):
    indices = pd.Series(data.index, index=data['movie_id'])
    index = indices[movie_id]

    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]

    movie_indices = [i[0] for i in sim_scores]

    movie_id = data['movie_id'].iloc[movie_indices]
    movie_title = data['original_title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['Movie_Id', 'Name', 'Genres'])

    recommendation_data['Movie_Id'] = movie_id
    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres

    return recommendation_data


# Take a movie’s title as input and returns the top 20 recommendations in the form of a python dictionary
def get_ml_movies(movie_id):
    movie_id = str(movie_id)

    find_movie = get_data()
    combine_result = combine_data(find_movie)
    transform_result = transform_data(combine_result, find_movie)

    if movie_id not in find_movie['movie_id'].unique():
        return []

    else:
        recommendations = recommend_movies(movie_id, find_movie, combine_result, transform_result)
        return recommendations.to_dict('records')
