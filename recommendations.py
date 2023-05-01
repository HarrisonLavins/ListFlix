import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Get information about a movie from dataset to be used for further preprocessing
def get_data():
    movie_data = pd.read_csv('dataset/movie_data.csv')
    movie_data['movie_id'] = movie_data['movie_id']
    return movie_data


# Drop the columns not used for feature extraction and combine cast and genres; return the combined column

def combine_data(data):
    # Drop attributes not required for feature extraction
    data_recommend = data.drop(columns=['movie_id', 'original_title', 'plot'])
    # Combine cast and genre into combine column
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(
        lambda x: ','.join(x.dropna().astype(str)), axis=1)
    data_recommend = data_recommend.drop(columns=['cast', 'genres'])
    return data_recommend


# Take the value returned by combine_data() and the plot column from get_data() and
# apply CountVectorizer and TfidfVectorizer respectively and calculates the Cosine values.
def transform_data(data_combine, data_plot):
    # Make object for CountVectorizer
    count = CountVectorizer(stop_words='english')
    # Fit CountVectorizer object count onto combine column
    count_matrix = count.fit_transform(data_combine['combine'])
    # Make an object for TfidfVectorizer and remove English stopwords
    tfidf = TfidfVectorizer(stop_words='english')
    # Fit TfidfVectorizer onto plot column
    tfidf_matrix = tfidf.fit_transform(data_plot['plot'])
    # Combine the previous two spare matrices
    combine_sparse = sp.hstack([count_matrix, tfidf_matrix], format='csr')
    # Apply Cosine Similarity on the combined matrix
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    # Return array with Cosine Similarity values
    return cosine_sim


# Recommend movies. The function recommend_movies() takes four parameters:
# title (name of the movie), data (return value of get_data()), combine (return value of combine_data()) and,
# transform (return value of transform_data()). It returns a Pandas DataFrame with the top 20 movie recommendations
def recommend_movies(movie_id, data, combine, transform):
    # Create Pandas Series with indices of all movies in our dataset
    indices = pd.Series(data.index, index=data['movie_id'])
    # Get the index of the input movie that is passed in recommend_movies() function in the movie_id parameter.
    index = indices[movie_id]
    # Store Cosine Similarity values of each movie with respect to the input movie
    sim_scores = list(enumerate(transform[index]))
    # Sort in reverse order; we want the higher Cosine Similarity values
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Store the top 20 movies
    sim_scores = sim_scores[1:21]

    movie_indices = [i[0] for i in sim_scores]
    # Store the movie indices with their columns
    movie_id = data['movie_id'].iloc[movie_indices]
    movie_title = data['original_title'].iloc[movie_indices]
    movie_genres = data['genres'].iloc[movie_indices]
    # Create Pandas DataFrame with Movie_Id, Name, and Genres as columns
    recommendation_data = pd.DataFrame(columns=['Movie_Id', 'Name', 'Genres'])
    # Store all 20 movies similar to our input movie in the Pandas DataFrame
    recommendation_data['Movie_Id'] = movie_id
    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres
    # Return the DataFrame
    return recommendation_data


# Take a movie’s title as input and returns the top 20 recommendations in the form of a python dictionary
def get_ml_movies(movie_id):
    # Take a movie as input; analysis will be performed with respect to this movie
    movie_id = str(movie_id)
    # Get all the data from previous functions
    find_movie = get_data()
    combine_result = combine_data(find_movie)
    transform_result = transform_data(combine_result, find_movie)
    # Check if the input movie is in our dataset
    if movie_id not in find_movie['movie_id'].unique():
        return []
    # Otherwise perform the analysis and return recommendations as a Python dictionary
    else:
        recommendations = recommend_movies(movie_id, find_movie, combine_result, transform_result)
        return recommendations.to_dict('records')
