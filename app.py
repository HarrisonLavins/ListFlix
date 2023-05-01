from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from sqlscripts.mySQLFunctions import *
# from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from util.tmdb_api import *
from recommendations import get_ml_movies

app = Flask(__name__)

# Define Index
@app.route('/')
def index():
    # Create a session
    session['userID'] = None
    # Direct users to users page if logged in; if not redirect to login page
    loggedIn = session.get('accountID')
    if loggedIn:
        users = select_from_listUser([session['accountID']])
        return render_template('users.html', users=users)
    else:
        return redirect(url_for('login'))
    

# Define Homepage
@app.route('/home/<string:id>/')
# Function used to populate pages with movies; The machine learning algorithm connects here
def fetch_movies(id):
    session['userID'] = id

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
            # print(movie)
            # print('TRYING TO PRINT MOVIE ID')
            # print(movie['Movie_Id'])
            movie_details = getMovieDetailsById(str(movie["Movie_Id"]))
            movie_obj = {'original_title': movie_details['original_title'], 'poster_path': movie_details['poster_path'], 'overview': movie_details['overview']}
            ml_recommendations.append(movie_obj)
        
        ml_movie_list.append({'watched_movie_title': watched_movie_title, 'recommended_movies': ml_recommendations})

    #print('ml_movie_list --------------------------')
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
    print(user)

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


    # Get some default IMDB Discover movies for Browse tab
    discoverMovies = getDiscover()

    # Pass the home template page a Python dictionary called 'movies'
    return render_template("library.html", movies=movie_watched_list, hidden_movies=movie_hidden_list, user=user[0], discoverMovies=discoverMovies)

# Add user page form
class NewUserForm(Form):
    username = StringField('Username', [validators.Length(min=2, max=25)])

# Add user page
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = NewUserForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        profilepic = request.form['profilepic']
        
        try: 
            accountID = session['accountID']
            insert_into_listUser(username, profilepic, accountID)
        
            flash('Welcome, ' + username + ', you may now start adding movies!', 'success')

            redirecturl = f'/'
            return redirect(redirecturl)
        except:
            flash('Something went wrong', 'danger')
    return render_template('adduser.html', form=form)
    
# Register page form
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
    # Flask decorator used to prevent users from seeing parts of the web app if they aren't logged in
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



@app.route('/add-movie')
def add_movie():
    query_params = request.args.to_dict()
    print(query_params)
    userID = query_params['userID']
    tmdbID = query_params['tmdbID']
    # movieID = query_params['movieID']

    alreadyInDB = select_from_listMovie([tmdbID], 'tmdbID')

    # if movie is already in DB
    if len(alreadyInDB) > 0:
        movieTitle = alreadyInDB[0][2]
        movieID = alreadyInDB[0][0]

        try:
            insert_into_relUserMovie(userID, movieID, 0)

            flash('Successfully added ' + movieTitle + ' to your Watched List', 'success')
            url = f'/library/{userID}'
            return redirect(url)
        except:
            flash('An error occurred adding your movie, please try again later', 'danger')
            return redirect('/')
    else: 
        # movie is not already in DB, so add it
        movieDetails = getMovieDetailsById(tmdbID)
        print(movieDetails)
        try:
            insert_into_listMovie(tmdbID, movieDetails['original_title'], None, None, None)
            alreadyInDB = select_from_listMovie([tmdbID], 'tmdbID')
            movieID = alreadyInDB[0][0]
            insert_into_relUserMovie(userID, movieID, 0)

            flash('Successfully added ' + movieDetails['original_title'] + ' to your Watched List', 'success')
            url = f'/library/{userID}'
            return redirect(url)
        except:
            flash('An error occurred adding your movie, please try again later', 'danger')
            return redirect('/')
        

# Library Search feature
@app.route('/search/<string:query>/')
def search_tmdb(query):

    results = searchMovies(query)
    return results




if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
