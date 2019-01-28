from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Genre, Movies, Base

#Connect to database and create the session
engine = create_engine('sqlite:///moviegenre.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
  movies = session.query(Movies).filter_by(id = genre.id).all()
  return render_template('movies.html', genre = genre, movies = movies)

#Add new movie to a genre catagory
@app.route('/genres/<genre_type>/movies/new/')
def newMovie(genre_type):
  if request.method == 'POST':
    newMovie = Movies(title = request.form['title'], year = request.form['year'], plot = request.form['plot'], poster = request.form['poster'], genre_type = genre_type)
    session.add(newMovie)
    session.commit()
    flash('%s was added to the list successfully' % newMovie.title)
    return redirect(url_for('showMovies', genre_type = genre_type))
  else:
    return render_template('newMovie.html', genre_type = genre_type)

#Edit movie information
@app.route('/genres/<genre_type>/movies/<int:movie_id>/edit/')
def editMovie(genre_type, movie_id):
  editedMovie = session.query(Movies).filter_by(id = movie_id).one()
  genre = session.query(Genre).filter_by(type = genre_type).one()
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
@app.route('/genres/<genre_type>/movies/<int:movie_id>/delete/')
def deleteMovie(genre_type, movie_id):
  genre = session.query(Genre).filter_by(type=genre_type).one()
  movieToDelete = session.query(Movies).filter_by(id = movie_id).one()
  if request.method == 'POST':
    session.delete(movieToDelete)
    session.commit()
    flash('Movie successfully deleted.')
    return redirect(url_for(showMovies, genre_type = genre_type))
  else:
    return render_template('deleteMovie.html', delete = movieToDelete)

  



if __name__ == '__main__':
  app.secret_key = 'secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)