from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from sqlscripts.mySQLFunctions import *
# from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from util.tmdb_api import *
from recommendations import get_ml_movies

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
    users = select_from_listUser([session['accountID']])
    return render_template('users.html', users=users)

@app.route('/home/<string:id>/')
def fetch_movies(id):
    # Create object with user information
    user = select_from_listUser([id],'id')
    # user = select_from_listUser([session['UserID']],'id')
    
    movie_watched_list = []
    rum = select_from_relUserMovie(id,'0')
    print(rum)
    for m_tuple in rum:
        movie_watched_list.append(m_tuple[0])


    # Call TMDB API for each watched movie
    tmbd_movie_list = []
    for tmdbID in movie_watched_list:
        print(tmdbID, type(tmdbID))
        recommended_movies = getRecommendedMoviesById(tmdbID)
        watched_movie_title = select_from_listMovie([tmdbID], 'tmdbID')[0][2]
        tmbd_movie_list.append({'watched_movie_title': watched_movie_title,'recommended_movies': recommended_movies})


    #Get ML Recommended Movies
    ml_movie_list = []

    for tmdbID in movie_watched_list:
        # print(tmdbID, type(tmdbID))
        watched_movie_title = select_from_listMovie([tmdbID], 'tmdbID')[0][2]

        ml_recommendations = []
        ml_recommended_movies = get_ml_movies(tmdbID)
        for movie in ml_recommended_movies:
            print(movie)
            print('TRYING TO PRINT MOVIE ID')
            print(movie['Movie_Id'])
            movie_details = getMovieDetailsById(str(movie["Movie_Id"]))
            movie_obj = {'original_title': movie_details['original_title'], 'poster_path': movie_details['poster_path'], 'overview': movie_details['overview']}
            ml_recommendations.append(movie_obj)
        
        ml_movie_list.append({'watched_movie_title': watched_movie_title, 'recommended_movies': ml_recommendations})

    print('ml_movie_list --------------------------')
    # print(ml_movie_list[0])


    # Pass the home template page a Python dictionary called 'movies'
    return render_template("home.html", movies=tmbd_movie_list, ml_movies=ml_movie_list, user=user[0])

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
class NewUserForm(Form):
    username = StringField('Username', [validators.Length(min=2, max=25)])
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = NewUserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        profilepic = request.form['profilepic']
        
        try: 
            accountID = session['accountID']
            insert_into_listUser(username, profilepic, accountID)
        
            flash('Welcome,' + username + ', you may now start adding movies!', 'success')

            redirecturl = f'/'
            return redirect(redirecturl)
        except:
            flash('Something went wrong', 'danger')
    return render_template('adduser.html', form=form)
    
# Register From Class
class RegisterForm(Form):
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
        
        profilepic = request.form['profilepic']
        
        if "@" in email:
            try: 
                insert_into_listAccount(email, password)
                result = select_from_listAccount([email])
                accountID = result[0]
                insert_into_listUser(username, profilepic, accountID)
            
                flash('You are now registered and can log in', 'success')

                # Log the user in once registered
                session['logged_in'] = True
                session['accountID'] = accountID

                redirecturl = f'/'
                return redirect(redirecturl)
            except:
                flash('That email already exists', 'danger')
        else:
            flash('Not a real email!','danger')
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
    
        result = select_from_listAccount([email])
        # print(result)
        
        if not result:
            error = 'Email not found'
            return render_template('login.html', error=error)
        else:
            accountID = result[0]
            password = result[1]
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['accountID'] = accountID
                # session['userId'] = 
    
                flash('You are now logged in', 'success')
                # redirecturl = f'/home/{result[0][0]}/'
                redirecturl = f'/'
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

# Library Search feature

@app.route('/search/<string:query>/')
def render_library(query):

    results = searchMovies(query)
    return results




if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
