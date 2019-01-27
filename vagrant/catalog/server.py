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
@app.route('/genres/<str:genre_type>/')
@app.route('/genres/<str:genre_type>/movies/')
def showMovies(genre_type):
  genre = session.query(Genre).filter_by(type = genre_type).one()
  movies = session.query(Movies).filter_by(genre_type = genre_type).all()
  return render_template('movies.html', genre = genre, movies = movies)

#Add new movie to a genre catagory
@app.route('/genres/<str:genre_type>/movies/new/')
def newMovie(genre_type):
  if request.method == 'POST':
    newMovie = Movies(title = request.form['title'], year = request.form['year'], plot = request.form['plot'], poster = request.form['poster'], genre_type = genre_type)
    session.add(newMovie)
    session.commit()
    flash('%s was added to the list successfully' % newMovie.title)
    return redirect(url_for('showMovies', genre_type = genre_type))
  else:
    return render_template('newMovie.html', genre_type = genre_type)

  



if __name__ == '__main__':
  app.secret_key = 'secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
