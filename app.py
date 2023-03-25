from flask import Flask, render_template
import urllib.request, json
from config import api_key
from sqlscripts.mySQLFunctions import *
# from flask_mysqldb import MySQL
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators, request
# from passlib.hash import sha256_crypt

app = Flask(__name__)

# # Config MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'ET_5600'
# app.config['MYSQL_DB'] = 'LISTFLIX'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#
# # initialize MYSQL
# mysql = MySQL(app)

def getMoviesByUrl(url):
    # Get data from TMDB API
    response = urllib.request.urlopen(url)
    data = response.read()
    movie_data = json.loads(data)
    return movie_data["results"]

def getDiscover():
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'

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

@app.route('/')
def index():
    return render_template('users.html')

@app.route('/home/<string:id>/')
def fetch_movies(id):
    # Create object with user information
    user = {'id': id}

    user_movies = []

    # Call TMDB API for each watched movie
    # movie_watched_list = [33, 11, 17, 26]
    movie_watched_list = []
    tmdbIDs = select_from_relUserMovie(['3'])
    for i in tmdbIDs:
        movie_watched_list.append(tmdbIDs[0])
    for tmdbID in movie_watched_list:
        user_movies.append(getRecommendedMoviesById(tmdbID))


    # Pass the home template page a Python dictionary called 'movies'
    return render_template("home.html", movies=user_movies, user=user)










#
# Register From Class
# class RegisterForm(Form):
#     name = StringField('Name', [validators.Length(min=1, max=50)])
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email', [validators.Length(min=6, max=50)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')
#     ])
#     confirm = PasswordField('Confirm Password')
# User Register
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email = form.email.data
#         username = form.username.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#
#         cur = mysql.connection.cursor()
#
#         cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
#
#         mysql.connection.commit()
#
#         cur.close()
#
#         flash('You are now registered and can log in', 'success')
#
#         return render_template('register.html')
#     return render_template('register.html', form=form)
#
# User login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
    # if request.method == 'POST':
    #     # Get Form Fields
    #     username = request.form['username']
    #     password_candidate = request.form['password']
    #
    #     # Create cursor
    #     cur = mysql.connection.cursor()
    #
    #     # Get user by username
    #     result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    #
    #     if result > 0:
    #         # Get stored hash
    #         data = cur.fetchone()
    #         password = data['password']
    #
    #         # Compare Passwords
    #         if sha256_crypt.verify(password_candidate, password):
    #             # Passed
    #             session['logged_in'] = True
    #             session['username'] = username
    #
    #             flash('You are now logged in', 'success')
    #             return redirect(url_for('dashboard'))
    #         else:
    #             error = 'Invalid login'
    #             return render_template('login.html', error=error)
    #         # Close connection
    #         cur.close()
    #     else:
    #         error = 'Username not found'
    #         return render_template('login.html', error=error)
    #
#    return render_template('login.html')

# Check if user logged in
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Unauthorized, Please login', 'danger')
#             return redirect(url_for('login'))
#     return wrap

#Logout
# @app.route('/logout')
# @is_logged_in
# def logout():
#     session.clear()
#     flash('You are now logged out', 'success')
#     return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)