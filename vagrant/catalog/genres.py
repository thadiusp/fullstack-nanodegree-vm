from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Movies, User, Base

engine = create_engine('sqlite:///moviegenre.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name="Thadius Pitts", email="thadiusp@gmail.com",
             picture="https://plus.google.com/u/0/photos/103218012335929749437/albums/profile/6209413327849053954?iso=false")
session.add(user1)
session.commit()

genre1 = Genre(user_id=1, type="Action")

session.add(genre1)
session.commit()

movie1 = Movies(user_id=1, title="John Wick", year="2014",
                plot="An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.",
                poster="https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX300.jpg", type="Action")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title='Batman Begins', year='2005',
                plot='After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption.',
                poster='https://m.media-amazon.com/images/M/MV5BZmUwNGU2ZmItMmRiNC00MjhlLTg5YWUtODMyNzkxODYzMmZlXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg', type="Action")
session.add(movie2)
session.commit()

genre2 = Genre(user_id=1, type="Adventure")

session.add(genre2)
session.commit()

movie1 = Movies(user_id=1, title="The Bourne Identity", year="2002",
                plot="A man is picked up by a fishing boat, bullet-riddled and suffering from amnesia, before racing to elude assassins and attempting to regain his memory.",
                poster="https://m.media-amazon.com/images/M/MV5BM2JkNGU0ZGMtZjVjNS00NjgyLWEyOWYtZmRmZGQyN2IxZjA2XkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SX300.jpg", type="Adventure")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title="Elysium", year="2013",
                plot="In the year 2154, the very wealthy live on a man-made space station while the rest of the population resides on a ruined Earth. A man takes on a mission that could bring equality to the polarized worlds.",
                poster="https://m.media-amazon.com/images/M/MV5BNDc2NjU0MTcwNV5BMl5BanBnXkFtZTcwMjg4MDg2OQ@@._V1_SX300.jpg", type="Adventure")
session.add(movie2)
session.commit()

genre3 = Genre(user_id=1, type="Comedy")

session.add(genre3)
session.commit()

movie1 = Movies(user_id=1, title='Dumb and Dumber', year="1994",
                plot="The cross-country adventures of 2 good-hearted but incredibly stupid friends.",
                poster='https://m.media-amazon.com/images/M/MV5BZDQwMjNiMTQtY2UwYy00NjhiLTk0ZWEtZWM5ZWMzNGFjNTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg', type="Comedy")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title='Blockers', year='2018',
                plot="Three parents try to stop their daughters from losing their virginity on prom night.",
                poster="https://m.media-amazon.com/images/M/MV5BMjE0ODIzNjkzMl5BMl5BanBnXkFtZTgwODQ3MzU4NDM@._V1_SX300.jpg", type="Comedy")
session.add(movie2)
session.commit()

genre4 = Genre(user_id=1, type="Drama")

session.add(genre4)
session.commit()

movie1 = Movies(user_id=1, title="The Departed", year="2006",
                plot="An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
                poster="https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_SX300.jpg", type="Drama")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title="The Wolf of Wall Street", year="2013",
                plot="Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.",
                poster="https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_SX300.jpg", type="Drama")
session.add(movie2)
session.commit()


genre5 = Genre(user_id=1, type="Romance")

session.add(genre5)
session.commit()

movie1 = Movies(user_id=1, title="You've Got Mail", year="1998",
                plot="Two business rivals who despise each other in real life unwittingly fall in love over the Internet.",
                poster="https://m.media-amazon.com/images/M/MV5BZTcxNzgzZjMtYzZiZC00MmE1LTg3MzQtZDAxMTYyZWE4MDNhL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg", type="Romance")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title="The Notebook", year="2004",
                plot="A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences.",
                poster="https://m.media-amazon.com/images/M/MV5BMTk3OTM5Njg5M15BMl5BanBnXkFtZTYwMzA0ODI3._V1_SX300.jpg", type="Romance")
session.add(movie2)
session.commit()

genre6 = Genre(user_id=1, type="SciFi")

session.add(genre6)
session.commit()

movie1 = Movies(user_id=1, title="Star Wars", year="1977",
                plot="Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.",
                poster="https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg", type="SciFi")
session.add(movie1)
session.commit()

movie2 = Movies(user_id=1, title="Star Trek", year="2009",
                plot="The brash James T. Kirk tries to live up to his father's legacy with Mr. Spock keeping him in check as a vengeful Romulan from the future creates black holes to destroy the Federation one planet at a time.",
                poster="https://m.media-amazon.com/images/M/MV5BMjE5NDQ5OTE4Ml5BMl5BanBnXkFtZTcwOTE3NDIzMw@@._V1_SX300.jpg", type="SciFi")
session.add(movie2)
session.commit()

print('Genres & movies were successfully added!')
