from flask import Flask, render_template
import urllib.request, json
from config import api_key

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('users.html')

@app.route('/home/<string:id>/')
def fetch_movies(id):
    # Create object with user information
    user = {'id': id}

    # Use TMDB discover page to fetch random movies from API
    # url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'

    # Replace this URL to display different API results on the user home page
    url = 'https://api.themoviedb.org/3/movie/245891/recommendations?api_key=71fd409b351004d729d92c7280888cda&language=en-US&page=1'

    # Get data from API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)

    # Can uncomment below line for debugging, and to see what useful info TMDB API returns
    print(movie_data["results"][0]) 

    # Pass the home template page a Python dictionary called 'movies'
    return render_template("home.html", movies=movie_data["results"], user=user)

if __name__ == '__main__':
    app.run(debug=True)