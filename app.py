from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from sqlscripts.mySQLFunctions import *
# from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from util.tmdb_api import *
import recommendations

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


@app.route('/')
def index():
    return render_template('users.html')

@app.route('/home/<string:id>/')
def fetch_movies(id):
    # Create object with user information
    user = select_from_listUser([id], 'id')
    
    user_movies = []

    # Call TMDB API for each watched movie
    movie_watched_list = []
    rum = select_from_relUserMovie(id,'0')
    for m_tuple in rum:
        movie_watched_list.append(m_tuple[0])
    for tmdbID in movie_watched_list:
        recommended_movies = getRecommendedMoviesById(tmdbID)
        watched_movie_title = select_from_listMovie([tmdbID], 'tmdbID')
        user_movies.append({'watched_movie_title': watched_movie_title,'recommended_movies': recommended_movies})

    # Pass the home template page a Python dictionary called 'movies'
    return render_template("home.html", movies=user_movies, user=user[0])

@app.route('/library/<string:id>/')
def render_library(id):

    # TODO: Somehow set the path to the currently selected user clicked on in the "Users" page,
    # which maybe sets the session["selected_userId"] = userId
    # and can be accessed here to select the correct user library info


    # Create object with user information
    user = select_from_listUser([id], 'id')

    # Call TMDB API for each watched movie - NOT HIDDEN
    movie_watched_list = []
    rum = select_from_relUserMovie(id,'0')
    for m_tuple in rum:
        tmdb_id = m_tuple[0]
        movie_data = getMovieDetailsById(tmdb_id)

        # Construct movie object - ToDo: move logic to helper function
        movie_obj = {'movie_title': movie_data["original_title"], 'overview': movie_data["overview"], 'poster_path': movie_data["poster_path"]}

        movie_watched_list.append(movie_obj)

    # Call TMDB API for each watched movie - NOT HIDDEN
    movie_hidden_list = []
    hidden_movies = select_from_relUserMovie(id,'1')
    for m_tuple in hidden_movies:
        tmdb_id = m_tuple[0]
        movie_data = getMovieDetailsById(tmdb_id)

        # Construct movie object - ToDo: move logic to helper function
        hidden_movie_obj = {'movie_title': movie_data["original_title"], 'overview': movie_data["overview"], 'poster_path': movie_data["poster_path"]}

        movie_hidden_list.append(hidden_movie_obj)

    # Pass the home template page a Python dictionary called 'movies'
    return render_template("library.html", movies=movie_watched_list, hidden_movies=movie_hidden_list, user=user[0])

# Register From Class
class RegisterForm(Form):
    #name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=2, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        insert_into_listUser(email,username,password)
        
        flash('You are now registered and can log in', 'success')

        # Log the user in once registered
        session['logged_in'] = True
        session['username'] = username

        return render_template('users.html')
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
    
        result = select_from_listUser([username], 'user')
        print(result)
        
        if not result:
            error = 'Username not found'
            return render_template('login.html', error=error)
        else:
            password = result[0][3]
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                # session['userId'] = 
    
                flash('You are now logged in', 'success')
                redirecturl = f'/home/{result[0][0]}/'
                return redirect(redirecturl)
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
    
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# @app.route('/movie', methods=['GET'])
# def recommend_movies():
#     res = recommendations.results(request.args.get('title'))
#     return jsonify(res)

# @app.route('/recommend', methods=['GET', 'POST'])
# def recommend():
#     if request.method == 'POST':
#         # Get the user input from the form
#         user_input = request.form['movie']
#         # Use the model to generate recommendations based on the user input
#         res = recommendations.results(user_input)
#         # Return the recommendations as a dictionary
#         #return {'recommendations': recommendations}
#         return jsonify(res)
#     else:
#         # Render the recommend template on a GET request
#         return render_template('recommend.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
