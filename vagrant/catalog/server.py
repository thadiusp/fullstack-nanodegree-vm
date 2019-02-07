from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Genre, Movies, User, Base

#Oauth imports
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

#Connect to database and create the session
engine = create_engine('sqlite:///moviegenre.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create token and store in login session
@app.route('/login')
def showLogin():
  state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
  login_session['state'] = state
  return render_template('login.html', state=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
  if request.args.get('state') != login_session['state']:
    return jsonify('Invalid state parimeter'), 401
  #Obtain authorization code
  code = request.database

  try:
    #Upgrade authorization code to a credentials object
    oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    return jsonify('Failed to upgrade the authorization code'), 401

  #Check the validity of the access_code
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

  #Abort if access token error
  if result.get('error') is not None:
    return jsonify('Error'), 500

  #Verify access token is used for intended user
  google_id = credentials.id_token['sub']
  if result['user_id'] != google_id:
    return jsonify('Token users id does not match given user id'), 401

  #Verify app validity for this access token
  if result['issued_to'] != CLIENT_ID:
    return jsonify('Token client ID does not match App'), 401

  #Check if user is already logged in
  stored_credentials = login_session.get('access_token')
  stored_google_id = login_session.get('goole_id')
  if stored_credentials is not None and google_id == stored_google_id:
    return jsonify('Current user is already connected'), 200

  #Store the access token for later session usage
  login_session['access_token'] = credentials.access_token
  login_session['google_id'] = google_id

  #Gather Users info
  userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
  params = {'access_token': credentials.access_token, 'alt':'json'}
  answer = requests.get(userinfo_url, params=params)
  data = answer.json()

  login_session['username'] = data['name']
  login_session['picture'] = data['picture']
  login_session['email'] = data['email']

  user_id = getUserID(login_session['email'])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id

  output = ''
  output += '<h1>Welcome'
  output += login_session['username']
  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output += '" style="width: 150px; height: 150px; border-radius: 150px; -webkit-border-radius: 150px; -moz=border-radius: 150px;">'
  flash("You are now logged in as %s" % login_session['username'])
  return output

#Create a user
def createUser(login_session):
  newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email=login_session['email']).one()
  return user.id

def getUserInfo(user_id):
  user = session.query(User).filter_by(id=user_id).one()
  return user

def getUserID(email):
  try:
    user = session.query(User).filter_by(email=email).one()
    return user
  except:
    return None























#Homepage (Shows all genres)
@app.route('/')
@app.route('/genres')
def showGenres():
  genres = session.query(Genre).order_by(asc(Genre.type))
  return render_template('genres.html', genres = genres)

#Show movies in picked genre
@app.route('/genres/<genre_type>/')
@app.route('/genres/<genre_type>/movies/')
def showMovies(genre_type):
  genre = session.query(Genre).filter_by(type = genre_type).one()
  movies = session.query(Movies).filter_by(type = genre_type).all()
  contributor = getUserInfo(movies.user_id)
  if 'username' not in login_session or contributor.id != login_session['user_id']:
    return render_template('publicMovies.html', genre = genre, movies = movies, contributor = contributor)
  else:
    return render_template('movies.html', genre = genre, movies = movies, contributor = contributor)

#Add new movie to a genre catagory
@app.route('/genres/<genre_type>/movies/new/', methods=['GET', 'POST'])
def newMovie(genre_type):
  if 'username' not in login_session:
    return redirect('/login')
  if request.method == 'POST':
    genre = session.query(Genre).filter_by(type = genre_type).one()
    newMovie = Movies(title = request.form['title'], year = request.form['year'], plot = request.form['plot'], poster = request.form['poster'], type = genre_type)
    session.add(newMovie)
    session.commit()
    flash('%s was added to the list successfully' % newMovie.title)
    return redirect(url_for('showMovies', genre_type = genre_type))
  else:
    return render_template('newMovie.html', genre_type = genre_type)

#Edit movie information
@app.route('/genres/<genre_type>/movies/<int:movie_id>/edit/', methods=['GET', 'POST'])
def editMovie(genre_type, movie_id):
  editedMovie = session.query(Movies).filter_by(id = movie_id).one()
  genre = session.query(Genre).filter_by(type = genre_type).one()
  if 'username' not in login_session:
    return redirect('/login')
  if editedMovie.user_id != login_session['user_id']:
    return "<script>function alert() {alert('You are not Authorized to edit this movie.');}</script><body onload='alert()'>"
  if request.method == 'POST':
    if request.form['title']:
      editedMovie.title = request.form['title']
    if request.form['year']:
      editedMovie.year = request.form['year']
    if request.form['plot']:
      editedMovie.plot = request.form['plot']
    session.add(editedMovie)
    session.commit()
    flash('Movie has been updated.')
    return redirect(url_for('showMovies', genre_type = genre_type))
  else:
    return render_template('editMovie.html', edit=editedMovie, genre=genre)

#Delete movie from database
@app.route('/genres/<genre_type>/movies/<int:movie_id>/delete/', methods=['GET', 'POST'])
def deleteMovie(genre_type, movie_id):
  genre = session.query(Genre).filter_by(type=genre_type).one()
  movieToDelete = session.query(Movies).filter_by(id = movie_id).one()
  if 'username' not in login_session:
    return redirect('/login')
  if deleteMovie.user_id != login_session['user_id']:
    return "<script>function alert() {alert('You are not Authorized to delete this movie.');}</script><body onload='alert()'>"
  if request.method == 'POST':
    session.delete(movieToDelete)
    session.commit()
    flash('Movie successfully deleted.')
    return redirect(url_for('showMovies', genre_type = genre_type))
  else:
    return render_template('deleteMovie.html', delete = movieToDelete, genre=genre)

  



if __name__ == '__main__':
  app.secret_key = 'secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
