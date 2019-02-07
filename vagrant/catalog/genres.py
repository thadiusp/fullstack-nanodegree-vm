from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Movies, User, Base

engine = create_engine('sqlite:///moviegenre.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(name="Thadius Pitts", email="thadiusp@gmail.com",
             picture="https://plus.google.com/u/0/photos/103218012335929749437/albums/profile/6209413327849053954?iso=false")
# Genre
genre1 = Genre(type="Action")

session.add(genre1)
session.commit()

movie1 = Movies(user_id=1, title="John Wick", year="2014", 
plot="An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.", 
poster="https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg")

session.add(movie1)
session.commit()

genre2 = Genre(type="Adventure")

session.add(genre2)
session.commit()

genre3 = Genre(type="Comedy")

session.add(genre3)
session.commit()

genre4 = Genre(type="Drama")

session.add(genre4)
session.commit()

genre5 = Genre(type="Romance")

session.add(genre5)
session.commit()

genre6 = Genre(type="SciFi")

session.add(genre6)
session.commit()

print('Genres were successfully added!')
