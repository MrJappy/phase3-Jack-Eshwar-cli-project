from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# set up the database connection
engine = create_engine('sqlite:///leaderboard.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# create a player class


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Integer)


# create the players table in the database
if __name__ == '__main__':
    Base.metadata.create_all(engine)
