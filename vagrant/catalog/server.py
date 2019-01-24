from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User





if __name__ == '__main__':
  app.secret_key = 'secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
