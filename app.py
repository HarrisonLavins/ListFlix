from flask import Flask, render_template
import urllib.request, json
from config import api_key

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fetch-movies')
def fetch_movies():
    # Use TMDB discover page to fetch random movies from API
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'

    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)

    # Can uncomment below line for debugging, and to see what useful info TMDB API returns
    # print(dict) 

    # Pass the fetch-movies template page a Python dictionary called 'movies'
    return render_template("fetch-movies.html", movies=movie_data["results"])

if __name__ == '__main__':
    app.run(debug=True)