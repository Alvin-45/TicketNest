from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)

class Seat(Base):
    __tablename__ = 'seat'

    movie_name = Column(String, index=True)
    seatnumber = Column(Integer,primary_key=True, unique=True, index=True)
    emailid = Column(String, unique=True, index=True)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    movie_name = Column(String, unique=True, index=True)