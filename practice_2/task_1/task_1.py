from sqlalchemy import Float, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)


class Base(DeclarativeBase):
    pass


class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True, index=True)
    name_genre = Column(String)


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, index=True)
    name_author = Column(String)


class City(Base):
    __tablename__ = 'cities'

    city_id = Column(Integer, primary_key=True, index=True)
    name_city = Column(String)
    days_delivery = Column(Integer)


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(ForeignKey("authors.author_id"))
    genre_id = Column(ForeignKey("genres.genre_id"))
    price = Column(Float)
    amount = Column(Integer)


class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    name_client = Column(Integer)
    city_id = Column(ForeignKey("cities.city_id"))
    email = Column(String)


class Buy(Base):
    __tablename__ = "buys"

    buy_id = Column(Integer, primary_key=True, index=True)
    buy_description = Column(String)
    client_id = Column(ForeignKey("clients.client_id"))
    email = Column(String)


class BuyBook(Base):
    __tablename__ = "buy_books"

    buy_book_id = Column(Integer, primary_key=True, index=True)
    book_id = Column(ForeignKey("books.book_id"))
    buy_id = Column(ForeignKey("buys.buy_id"))
    amount = Column(Integer)


class Step(Base):
    __tablename__ = "steps"

    step_id = Column(Integer, primary_key=True, index=True)
    name_step = Column(String)


class BuyStep(Base):
    __tablename__ = "buy_steps"

    buy_step_id = Column(Integer, primary_key=True, index=True)
    buy_id = Column(ForeignKey("buys.buy_id"))
    step_id = Column(ForeignKey("steps.step_id"))
    data_step_beg = Column(Integer)
    data_step_end = Column(Integer)


Base.metadata.create_all(engine)
