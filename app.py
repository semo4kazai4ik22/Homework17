# app.py

from flask import Flask, request
from flask_restx import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
import schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)
api = Api(app)
movies_ns = api.namespace("movies")

movies_schema = schema.Movie(many=True)
movie_schema = schema.Movie()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id: object = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movies_ns.route("/")
class MovieView(Resource):
    def get(self):
        movies = db.session.query(Movie)

        args = request.args

        director_id = args.get('director_id')

        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)

        genre_id = args.get('genre_id')

        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)

        movies_query = movies.all()

        return movies_schema.dump(movies_query), 200


@movies_ns.route("/<int:mid>")
class MovieViewId(Resource):
    def get(self, mid):
        movie = db.session.query(Movie).get(mid)

        if movie is None:
            return {}, 404

        return movie_schema.dump(movie), 200


if __name__ == '__main__':
    app.run(debug=True)
