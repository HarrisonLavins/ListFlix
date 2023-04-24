from config import api_key
import urllib.request, json

def getMoviesByUrl(url):
    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data["results"]

def getMovieDetailsById(movieId):
    url = f'https://api.themoviedb.org/3/movie/{movieId}?api_key={api_key}&language=en-US'

    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data

def getDiscover():
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'

    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data["results"]

def searchMovies(query):
    #remember to URL encode the query!!!

    # url = f'https://api.themoviedb.org/3/search/movie/?api_key={api_key}&language=en-US&page=1'
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={query}&page=1&include_adult=false'

    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data["results"]

def getRecommendedMoviesById(movieId):
    url = f'https://api.themoviedb.org/3/movie/{movieId}/recommendations?api_key={api_key}&language=en-US&page=1'

    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data["results"]