from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User

#Connect to database and create the session
engine = create_engine('sqlite:///moviegenre.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



if __name__ == '__main__':
  app.secret_key = 'secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
